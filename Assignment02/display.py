
import queue

from rich import print
from rich.columns import Columns
from rich import box
from rich import panel
from rich.panel import Panel
from datetime import datetime
from time import sleep
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from CPU import CPU
from IPU import IPU
from rrcpu import RoundRobinCPU

layout = Layout()

layout.split(
    Layout(name="main"),
    Layout(name="footer"))

layout["main"].split_row(
    Layout(name="upLeft"), 
    Layout(name="upRight")
    #direction="horizontal"
)

layout["footer"].split_row(
    Layout(name="downLeft"), 
    Layout(name="downRight")
    #direction="horizontal"
)

layout['upLeft'].ratio = 1
layout['upRight'].ratio = 1

def printDetails(termTable):
    runned = termTable
    LWT = runned[0][1]
    SWT = runned[0][1]
    totalWT = 0.0
    turnAroundTime = 0.0
    totalTAT = 0.0
    avWT = 0.0
    avgTAT = 0.0
    totalUse = 0
    avgUse = 0
    tatPercent = 0
    for i in runned:
        turnAroundTime = i[1]+ i[2]
        totalWT = totalWT + int(i[1])
        totalTAT = totalTAT+ turnAroundTime
        newWT = i[1]
        totalUse += i[3]
        if(newWT>LWT):
            LWT = newWT
        elif(newWT<LWT):
            SWT = newWT
           
    avgTAT = totalTAT/ len(runned)
    avWT = totalWT/ len(runned)
    avgUse = totalUse / len(runned)
    tatPercent = ((avgTAT/len(runned))/2)


    table3 = Table(title="Wait Times")
    table3.add_column("Shortest Wait Time", justify="center")
    table3.add_column("Longest Wait Time",justify="center")
    table3.add_column("Average Wait Time",justify="center")
    table3.add_row(str(SWT),str(LWT),str(avWT) , style= "cyan")

    with Live(layout, screen=True, redirect_stderr=False) as live:
        layout["downLeft"].update(table3)
   
    table2 = Table(title="Usage")
    table2.add_column("Average Turnaround Time",justify="center")
    table2.add_column("CPU usage",justify="center")
    table2.add_row(str(avgTAT), str(tatPercent), style= "purple")

    with Live(layout, screen=True, redirect_stderr=False) as live:
        layout["downRight"].update(table2)
        sleep(100)

'''
Class to print the processes
'''
class printProcesses:
    def __init__(self,procList):
        self.procList = procList

    def makeTable(self):
        table = Table(title="Current Processes")
        table.add_column("PID", justify="center")
        table.add_column("Job", justify="center")
        table.add_column("Current Status", justify="center")
        
        #listed = list(self.pList)
        if(not len(self.procList) ==0):
            for item in self.procList:
                pidNum = str(item[0])
                location = str(item[1])
                running = str(item[2])
                table.add_row(pidNum,location,running,style="green")

        return table

    def __rich__(self) -> Panel:
        return Panel(self.makeTable())


'''
Class to print the tables of terminated processes
'''
class printTerm:
    def __init__(self,procList):
        self.procList = procList

    def makeTable(self):
        table3 = Table(title="Done Jobs")
        table3.add_column("Process ID", justify="center")
        table3.add_column("Wait Time",justify="center")
        table3.add_column("Burst Time",justify="center")
        table3.add_column("Turnaround Time",justify="center")

        if(not len(self.procList) ==0):
            for item in self.procList:
                IDNum = str(item[0])
                waitTime = str(item[1])
                burstTime = str(item[2])
                usage = str(item[3])
                turnAroundTime = str(item[1]+item[2])
                table3.add_row(IDNum,waitTime,burstTime,turnAroundTime, style="red")
              
        return table3

    def __rich__(self) -> Panel:
        return Panel(self.makeTable())

processList = []

'''
Scheduler Function
Schedules jobs to the CPU and IO
'''    
def Scheduler(prioQ,cpuNum,ipuNum):

    ioQ = queue.PriorityQueue()
    terminated = []
    usage = 0
    #create a table for the processes
    cpuList = []
    ipuList = []
    for x in range (cpuNum):
        cpuList.append(CPU("cpu"+str(x)))

    for n in range (ipuNum):
        ipuList.append(IPU("ipu"+str(n)))

 
    #while there are jobs in the queue
    while ((not (prioQ.empty())) or (not (ioQ.empty()))):
        #check CPU usage
        for cpu in cpuList:
            if(cpu.busy):
                usage+=1
        
            #check to see if a CPU is not busy
            if((not cpu.busy) and (not (prioQ.empty()))):
                #send to CPU
                item = prioQ.get()
                cpu.assignProcess(item)
                processList.append((str(item.pID),cpu.name,"Processing"))     
        
            #actually run process on CPU
            cpu.tick()
    
            #if the process on the CPU1 requires IO
            if(cpu.curProcess.waiting):
                ioQ.put(cpu.curProcess)
                processList.append((str(cpu.curProcess.pID),"Wait Queue","Waiting"))
                
                cpu.clear()
                
            #else if the process has terminated
            elif (cpu.curProcess.done):
                #add to terminated list
                processList.append((str(cpu.curProcess.pID),cpu.name,"CPU Burst Completed"))
                terminated.append((cpu.curProcess.pID, cpu.curProcess.waitTime, cpu.curProcess.BT, usage))
                cpu.clear()
 
        #anything in the Ready Queue needs to have its waitTime increased
        for process in prioQ.queue:
            process.BT+=1
        
        for ipu in ipuList:
            #check to see if a IPU1 is not busy
            if((not ipu.busy) and (not (ioQ.empty()))):
                #send to IPU
                item = ioQ.get()
                ipu.assignProcess(item)
                processList.append((str(item.pID),ipu.name,"Processing IO"))

            #actually run process on I/O PU
            ipu.tick()

            #anything in the IO Queue needs to have its waitTime increased
            for process in ioQ.queue:
                process.waitTime+=1

            #has IPU1 finished I/O
            if(ipu.curProcess.ready):
                processList.append((str(ipu.curProcess.pID),"Ready Queue","Ready for CPU"))
                prioQ.put(ipu.curProcess)
                ipu.curProcess.BT+=1
                processList.append((str(ipu.curProcess.pID),ipu.name,"IO burst completed"))
                ipu.clear()  
        
        P = printProcesses(processList)
        T = printTerm(terminated)

        with Live(layout, screen=True, redirect_stderr=False) as live:
            layout["upLeft"].update(P)
            layout["upRight"].update(T)
            sleep(0.2)
            

    #Table is returned so that final calulations can be done
    return terminated


'''
Scheduler function for Round Robin
Schedules jobs to the CPU and IO
'''    
def RRScheduler(prioQ,cpuNum,ipuNum):

    ioQ = queue.PriorityQueue()
    terminated = []
    usage = 0
    #table for the processes
    cpuList = []
    ipuList = []

    for x in range (cpuNum):
        cpuList.append(RoundRobinCPU("cpu"+str(x)))

    for n in range (ipuNum):
        ipuList.append(IPU("ipu"+str(n)))
    
    #while there are jobs inthe queue
    while ((not (prioQ.empty())) or (not (ioQ.empty()))):
        #check CPU usage
        for cpu in cpuList:
            if(cpu.busy):
                usage+=1

            #check to see if a CPU is not busy
            if((not cpu.busy) and (not (prioQ.empty()))):
                #send to CPU
                item = prioQ.get()
                cpu.assignProcess(item)
                processList.append((str(item.pID),cpu.name,"Processing"))       
            #actually run process on CPU
            cpu.tick()
           
            #if the process on the CPU1 requires IO
            if(cpu.curProcess.waiting):
                ioQ.put(cpu.curProcess)
                processList.append((str(cpu.curProcess.pID),"Wait Queue","Waiting"))
                #table.add_row(str(cpu1.currentProcess.ID),"Wait Queue","Waiting",style="yellow" )
                cpu.clear()

            #else if the process has terminated
            elif (cpu.curProcess.done):
                #add to terminated list
                processList.append((str(cpu.curProcess.pID),cpu.name,"CPU Burst Completed"))
                terminated.append((cpu.curProcess.pID, cpu.curProcess.waitTime, cpu.curProcess.BT, usage))
                cpu.clear()     

            #Determine if anything needs to be preempted
            if(cpu.quantum == 0):
                cpu.preempt(prioQ)

        #anything in the Ready Queue needs to have its waitTime increased
        for process in prioQ.queue:
            process.BT+=1 

        for ipu in ipuList:
            #check to see if IPU1 is not busy
            if((not ipu.busy) and (not (ioQ.empty()))):
                #send to IPU
                item = ioQ.get()
                ipu.assignProcess(item)
                processList.append((str(item.pID),ipu.name,"Processing IO"))

            #actually run process on I/O PU
            ipu.tick()

            #anything in the IO Queue needs to have its waitTime increased
            for process in ioQ.queue:
                process.waitTime+=1
                
            #has IPU1 finished I/O
            if(ipu.curProcess.ready):
                processList.append((str(ipu.curProcess.pID),"Ready Queue","Ready for CPU"))
                prioQ.put(ipu.curProcess)
                ipu.curProcess.BT+=1
                processList.append((str(ipu.curProcess.pID),ipu.name,"IO burst completed"))
                ipu.clear() 

        P = printProcesses(processList)
        T = printTerm(terminated)

        with Live(layout, screen=True, redirect_stderr=False) as live:
            layout["upLeft"].update(P)
            layout["upRight"].update(T)
            sleep(0.2)
    
    return terminated