#from rich import print
from collections.abc import MutableMapping
from random import randint

class Register:
    def __init__(self):
        self.contents = 0

    def write(self,x):
        self.contents = x

    def read(self):
        return self.contents

    def __str__(self):
        return f"[{self.contents}]"

    def __repr__(self):
        return self.__str__()

class Registers(MutableMapping):
    def __init__(self,num=2):
        self.num = num
        self.registers = []
        for i in range(num):
            self.registers.append(Register())
    def __setitem__(self, k, v):
        if isinstance(k,int):
            #setattr(self, self.registers[k], v)
            self.registers[k].write(v)
    def __getitem__(self, k):
        if isinstance(k,int):
        #getattr(self, k)
            return self.registers[k].read()
        return None
    def __len__(self):
        return self.num
    def __delitem__(self, k):
        if isinstance(k,int):
            self.registers[k] = None
    def __iter__(self):
        yield self.registers

    def __str__(self):
        s = ""
        for r in self.registers:
            s += "["+str(r)+"]"
        return s

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    reg = Registers(4)

    for i in range(len(reg)):
        reg[i] = randint(1,100)

    for r in reg:
        print(r)

