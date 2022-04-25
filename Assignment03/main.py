from random import shuffle
from random import seed
from random import randint
import json
#from rich import print 
import sys
from registers import Registers
import threading
import time
from time import sleep
from random import shuffle
from datetime import datetime
import datetime
import rwlock


from rwlock import * 

LOCK = RWLock()


Reader_Thread = []
Writer_Thread = []
stop_reader = False

mem = None
put_file = "memory1.json"

with open(put_file) as f:
    mem = json.load(f)  

registers = Registers(2)

Lock_entire = False


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

def reader(file):
  
    instructions = []
    
    with open(file) as f:
        instructions = json.load(f)
        #print(instructions)
    
    
    for insts in instructions:
      
        #acquire
        LOCK.reader_acquire()
        for inst in insts:
            #print(inst)
    #seperating instructions into TYPE(Read/Write), MemoryLocation(A100) and Register(R1/R2)
            i,loc,reg = inst.split()
    
            #print(f"{inst} {loc} {reg} ")
            # breaking up inst
            memBlock = loc[0]
            memAddr = loc[1:]
            register = int(reg[1]) -1
      

            #print(f"{memBlock} {memAddr}")

            # loads registers 
            if i == "READ":
                #print("Reader is Reading")
                registers[register] = mem[memBlock][memAddr]
                      
        LOCK.reader_release()
        sleep(0.5)
    sleep(1)
        # release
    #print(mem)
              
                  
#print(mem)
def reader_Segments(file):
    instructions = []
    
    with open(file) as f:
        instructions = json.load(f)
        #print(instructions)
    
    
    for insts in instructions:
        #acquire
        for inst in insts:
            #print(inst)

            i,loc,reg = inst.split()
    
            #print(f"{inst} {loc} {reg} ")
            # breaking up inst
            memBlock = loc[0]
            memAddr = loc[1:]
            register = int(reg[1]) -1

            if stop_reader:
              break
            
            if memBlock == "A":
              LOCK.reader_acquire()
              #print("Reading from A")
              if i == "READ":
                #print("Reader is Reading")
                registers[register] = mem[memBlock][memAddr]
                LOCK.reader_release()
                sleep(0.5)
                
            if memBlock == "B":
              
              LOCK.reader_acquire()
              #print("Reading from B")
              if i == "READ":
                #print("Reader is Reading")
                registers[register] = mem[memBlock][memAddr]
                LOCK.reader_release()
                sleep(0.5)
                  
            if memBlock == "C":
             
              LOCK.reader_acquire()
              #print("Reading from C")
              if i == "READ":
                #print("Reader is Reading")
                registers[register] = mem[memBlock][memAddr]
                LOCK.reader_release()
                sleep(0.5)


            if memBlock == "P":
             
              LOCK.reader_acquire()
              #print("Reading from C")
              if i == "READ":
                #print("Reader is Reading")
                registers[register] = mem[memBlock][memAddr]
                LOCK.reader_release()
                sleep(0.5)


        
        # release
    return (mem)
    #print(mem)
              
                  
#print(mem)

def writer(file):
    
    instructions = []
    
    with open(file) as f:
        instructions = json.load(f)
        #print(instructions)
    
    
    for insts in instructions:
        #print(insts)
    
        #acquire
        LOCK.writer_acquire()
        for inst in insts:
            #print(inst)
        #seperating instructions into TYPE(Read/Write), MemoryLocation(A100) and Register(R1/R2)
            i,loc,reg = inst.split()
    
            
            # breaking up inst
            memBlock = loc[0]
            memAddr = loc[1:]
            register = int(reg[1]) -1

            

            # loads registers 
            if i == "READ":           
                registers[register] = mem[memBlock][memAddr]
                
            if i in ['ADD','SUB','MUL','DIV']:
                #print("arithmetic")
                registers[0] = OPS[i](registers[0],registers[1])
               

            if i == "WRITE":
                #print("Writer is writing")
                mem[memBlock][memAddr] = registers[0]
          
        LOCK.writer_release()
        sleep(0.5)
    sleep(1)
        # release
    #print(mem)
    return(mem)

def writer_Segments(file):

    instructions = []
    #WRITER = Writer()
    
    with open(file) as f:
        instructions = json.load(f)
        #print(instructions)
    
    
    for insts in instructions:
        #print(insts)
       
        #acquire
        for inst in insts:
            #print(inst)

            i,loc,reg = inst.split()
    
            #print(f"{inst} {loc} {reg} ")
            # breaking up inst
            memBlock = loc[0]
            memAddr = loc[1:]
            register = int(reg[1]) -1

            LOCK.writer_acquire()
            if memBlock == "A":
              
              # LOCK.writer_acquire()
              #print("Writing in A")
              if i == "READ":           
                  registers[register] = mem[memBlock][memAddr]
                
              if i in ['ADD','SUB','MUL','DIV']:
                #print("arithmetic")
                registers[0] = OPS[i](registers[0],registers[1])
              
              if i == "WRITE":
                #print("Writer is writing")
                mem[memBlock][memAddr] = registers[0]
            LOCK.writer_release()
            sleep(0.1)
                
            LOCK.writer_acquire()
            if memBlock == "B":
              # LOCK.writer_acquire()
              #print("Writing in B")
              if i == "READ":           
                  registers[register] = mem[memBlock][memAddr]
                
              if i in ['ADD','SUB','MUL','DIV']:
                #print("arithmetic")
                registers[0] = OPS[i](registers[0],registers[1])
              
              if i == "WRITE":
                #print("Writer is writing")
                mem[memBlock][memAddr] = registers[0]
                
            LOCK.writer_release()
            sleep(0.1)
          
            LOCK.writer_acquire()
            if memBlock == "C":
              # LOCK.writer_acquire()
              #print("Writing in C")
              if i == "READ":           
                  registers[register] = mem[memBlock][memAddr]
                
              if i in ['ADD','SUB','MUL','DIV']:
                #print("arithmetic")
                registers[0] = OPS[i](registers[0],registers[1])
              
              if i == "WRITE":
                #print("Writer is writing")
                mem[memBlock][memAddr] = registers[0]
            LOCK.writer_release()
            sleep(0.1)

            LOCK.writer_acquire()
            if memBlock == "P":
              # LOCK.writer_acquire()
              #print("Writing in C")
              if i == "READ":           
                  registers[register] = mem[memBlock][memAddr]
                
              if i in ['ADD','SUB','MUL','DIV']:
                #print("arithmetic")
                registers[0] = OPS[i](registers[0],registers[1])
              
              if i == "WRITE":
                #print("Writer is writing")
                mem[memBlock][memAddr] = registers[0]
            LOCK.writer_release()
            sleep(0.1)

            
      
    return mem
    
    
if __name__=='__main__':

    
    num_writers = int(sys.argv[1])
    num_readers = num_writers * 5

    # different_target = sys.argv[2]
    # if different_target == 1:
    #   different_target = reader_Segments
    # else:
    #   different_target = writer_Segments
  
    #start the timer here
    start_times = datetime.datetime.now()
    #Create threads for readers/writers for whole file
    for i in range(num_readers):
        Reader_Thread.append(threading.Thread(target=reader, args=(f"reader_{i}.exe",)))
      
    for i in range(num_writers):
        Writer_Thread.append(threading.Thread(target=writer, args=(f"writer_{i}.exe",)))
    #shuffle the threads
    shuffle(Reader_Thread)
    shuffle(Writer_Thread)
    #start each process
    for process in Reader_Thread:
      process.start()
    for process in Writer_Thread:
      process.start()

    for joins in Writer_Thread:
      joins.join()
    stop_reader = True
    end_times = datetime.datetime.now()
    print("Logging time = ",end_times - start_times)
  
    #create the new file and dump memory after locking and unlocking with readers
    display_memory = "memory_after.json"
    with open(display_memory, "w") as f:
      json.dump(mem, f, indent=4)
    
 
   

  
    