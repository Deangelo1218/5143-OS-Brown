from operator import index
from rich import print
from registers import *
from lock import Lock


def add(l, r):
    return l + r


def sub(l, r):
    return l - r


def mul(l, r):
    return l * r


def div(l, r):
    return l / r


class Alu(object):
    def __init__(self, registers):
        self.lhs = None
        self.rhs = None
        self.op = None
        self.registers = registers
        self.ops = {"ADD": add, "SUB": sub, "MUL": mul, "DIV": div}

    def exec(self, op):
        self.lhs = self.registers[0]
        self.rhs = self.registers[1]
        self.op = op.upper()
        ans = self.ops[self.op](self.lhs, self.rhs)
        self.registers[0] = ans

    def __str__(self):
        return f"{self.lhs} {self.op} {self.rhs}"


class Cpu:
    def __init__(self, registers, timeslice, memory):
        self.cache = []
        self.pc = 0
        self.registers = registers
        self.alu = Alu(registers)
        self.timeslice = timeslice
        self.memory = memory
        self.lock = Lock()

    def loadProcess(self, pcb):
        instructions = Pcb.currentInstruction()
        count = 0
        time = self.timeslice
        for instr in instructions:
            if (time >=0):

                self.lock.acquire()
                i,loc,reg = instr.split()
        
                #print(f"{inst} {loc} {reg} ")
                # breaking up inst
                memBlock = loc[0]
                memAddr = loc[1:]
                register = int(reg[1]) + 1

                if(i == "LOAD"):
                    index = int(reg[-1][-1]) - 1
                    self.registers[index] = register
                if(instr == instr[-1]):
                    self.lock.release()
                
                if(i == "READ"):
                    index = int(reg[-1][-1]) 
                    self.registers[index] = self.memory[memBlock][memAddr]
                
                if(i == "WRITE"):
                    index = int(reg[-1][-1]) 
                    self.memory[memBlock][memAddr] = self.registers[index]

                time -=1
                count +=1



            # if (time >=0):
            #     part = instr.split()
            #     self.lock.acquire()



    def __str__(self):
        return f"[{self.registers}{self.alu}]"


class Pcb(object):
    def __init__(self,processId,registers,instructions,state):
        self.processId = processId
        self.inst = instructions
        self.registers = registers
        self.current = instructions[0]
        self.state = state
        self.pc = 0
    
    def proccesId(self):
        return self.proccesId
    
    def currentInstruction(self):
        return self.current
    
    def register(self):
        return self.registers
    
    def setState(self,status):
        self.state = status
    
    def getState(self):
        if(len(self.inst) <= 0):
            return "Process Done"
        
        return self.state
    
    # def doneInstructions(self):
    #     self.pc += 1
    #     del 
    def __repr__(self) -> str:
        return f"ID: {self.pid},\n State: {self.pState},\n Priority: {self.Priority},\n Current Instruction: {self.currentInstruction}\n\n"


if __name__ == "__main__":
    reg = Registers(2)
    cpu = Cpu(reg)

    print(cpu)

    reg[0] = 33
    reg[1] = 41

    alu = Alu(reg)

    alu.exec("add")