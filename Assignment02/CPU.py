#!/usr/bin/python
import sys
import random
import threading, queue
import time
from datetime import datetime
from time import sleep
import random
import json
import sys,os

from Process import Process

'''
CPU class
Class that determines how an instance of a CPU functions
'''
class CPU:
    def __init__(self,text):
        self.busy = False
        self.timeLeft = 0
        self.currentProcess = Process(-1,-1, 1,[-1],[-1],-1,False)
        self.name = text
    
    def assignProcess(self,process):
        self.busy = True
        self.timeLeft = process.CPU_bursts[0]
        self.currentProcess = process
        self.currentProcess.CPU_bursts.pop(0)


    def tick(self):
        #if any process not to run
        if(self.currentProcess.ID == -1):
            return

        self.timeLeft-=1
        if(self.timeLeft == 0):
            if(len(self.currentProcess.IO_bursts)):
                self.currentProcess.waiting = True
                self.currentProcess.ready = False
            else:
                self.currentProcess.ready = False
                self.currentProcess.waiting = False
                self.currentProcess.done = True
            
            self.busy = False

    def clear(self):
        self.busy = False
        self.timeLeft = 0
        self.currentProcess = Process(-1,-1,-1,[-1],[-1],-1,False)