#from dis import Instruction
##from distutils.command.install_scripts import install_scripts
#from doctest import FAIL_FAST
import sys, json
#from Assignment04.main import PriorityLock
#from Assignment04.main import priority
#from Assignment04.main import PriorityLock
from alu import *
from lock import Lock
from registers import Registers
from random import random, randint
from randInstruction import RandInstructions
import queue
import threading
from random import shuffle
import time
from time import sleep
from datetime import datetime
import datetime
from lock import Lock
from rich.live import Live
from rich.table import Table




PROGRAM_THREADS = []
# RegularLock = Lock()
# PriorityLock = Lock()
registers = Registers(4)




with open("memory1.json") as f:
    memory = json.load(f)


RWTable = Table()
RWTable.add_column("ID")
RWTable.add_column("Status")
RWTable.add_column("Memory Block : Memory Address")
#Using locks

RegularLock = Lock()
PriorityLock = Lock()

#print(memory)

def ADD(a,b):
    return a+b

def SUB(a,b):
    return a-b

def MUL(a,b):
    return a*b

def DIV(a,b):
  try:
    return a/b
  except ZeroDivisionError:
    return 1

OPS = {
    "ADD":ADD,
    "SUB":SUB,
    "MUL":MUL,
    "DIV":DIV,
}


def program(file, id):
    instructions = []

    with open(file) as f:
        instructions = json.load(f)
    
    for inst in instructions:
        #print(inst)

        for insts in inst:
            priorityInstruction = False

            insts= insts.strip().split(" ")
            typeIns = insts[0]
            
            
            if priorityInstruction == False:
               
                time.sleep(random())
                #RWTable.add_row(f"[magenta]Thread {id} with no Priority","[magenta]Waiting for Lock",f"At Memory Location [magenta]{memBlock}:{memAdd}")
                #print(f"Thread {id} waiting for lock because not priority")
                RegularLock.wait()
                

            #print(typeIns)
            #"READ P225 R2",
        

                if typeIns == "READ":
                    #temp = insts[-1]
                    
                    temp = insts[-1].strip()[1:]
                    temp2 = int(temp) - 1
                    memBlock = insts[1].strip()[0]
                    memAdd = insts[1].strip()[1:]
                    RWTable.add_row(f"[magenta]Thread {id} with no Priority","[magenta]Waiting to read",f"At Memory Location [magenta]{memBlock}:{memAdd}")
                    #print(memAdd)
                    #sample = temp[1:]
                    #print(temp)
                    #print("HIIIIIIII")
                    registers[temp2] = memory[memBlock][memAdd]

                if typeIns in  ['ADD','SUB','MUL','DIV']:
                    
                    #print("arithmetic")
                    registers[0] = OPS[typeIns](registers[0],registers[1])
                

                if typeIns == "WRITE":
                    #print("Writer is writing")
                    RWTable.add_row(f"[magenta]Thread {id} with no Priority","[magenta]Waiting to write",f"At Memory Location [magenta]{memBlock}:{memAdd}")
                    memory[memBlock][memAdd] = registers[0]
               # time.sleep(random())

                    #print(memory[memBlock][memAdd])

                    #"LOAD 0 R3",
            #time.sleep(random())
            # RWTable.add_row(f"[red]Thread {id} with Priority","[red]Acquiring the Lock")
            #print(f"Thread {id} is a priority thread so it acquires the lock")
            #PriorityLock.acquire()
            if typeIns == "LOAD":
                RWTable.add_row(f"[red]Thread {id} with Priority","[red]Acquiring the Lock")
                PriorityLock.acquire()
                priorityInstruction = True
                temp = insts[1]
                final = int(insts[-1].strip()[1:]) - 1
                #print(temp, final)
                registers[final] = temp
                #print(registers[final])
           
                
                PriorityLock.release()
                RWTable.add_row(f"[green]Thread {id} with Priority","[green]Releasing the Lock",f"Loading {insts[1]} in Register {final}")
                #RWTable.add_row(f"[green]Thread {id} with Priority","[green]Releasing the Lock",f"Loading {temp} in Register {registers[final]}")
                #print(f"[green]Thread {id} with Priority","[green]Releasing the Lock",f"Loading {insts[1]} in Register {final}")
            time.sleep(random())


if __name__ == "__main__":

    #program("program_0.exe", 1)
    with Live(RWTable, refresh_per_second=4):
 

        for i in range(5):
            PROGRAM_THREADS.append(threading.Thread(target=program, args=(f"program_{i}.exe", i,)))
        
        shuffle(PROGRAM_THREADS)

        for process in PROGRAM_THREADS:
            process.start()
        
        for joins in PROGRAM_THREADS:
            joins.join()


