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

'''
Process Class
Takes the information for each job and creates a queue 
for each scheduling algorithm
'''
class Process:
    def __init__(self, arrTime, ID, Prio, cpuBursts, ioBursts, mode, ready):
        #instance variables
        self.arrTime = int(arrTime)
        self.ID = int(ID)
        self.Prio = int(Prio)
        self.CPU_bursts = []
        self.IO_bursts = []
        self.mode = int(mode)
        
        #process attributes
        self.ready = ready
        self.waiting = False
        self.done = False
        self.waitTime = 0
        self.burstTime = 0
        self.BT = 0

        for cburst in cpuBursts:
            self.CPU_bursts.append(int(cburst))

        for iburst in ioBursts:
            self.IO_bursts.append(int(iburst))

    #checking the arrival time for the priority queue
    def __gt__(self,other):
        if(self.mode == 0):
            if (self.arrTime > other.arrTime):
                return True
            elif(self.arrTime == other.arrTime):
                if(self.ID < other.ID):
                    return True       
            return False
        elif(self.mode == 1):
            if (self.CPU_bursts[0] > other.cpuBursts[0]):
                return True
            elif(self.CPU_bursts[0] == other.cpuBursts[0]):
                if(self.ID < other.ID):
                    return True       
            return False
        elif(self.mode == 2):
            if (self.Prio > other.Prio):
                return True
            elif(self.Prio == other.Prio):
                if(self.ID < other.ID):
                    return True       
            return False
        elif(self.mode == 3):
            if (self.CPU_bursts[0] > other.cpuBursts[0]):
                return True
            elif(self.CPU_bursts[0] == other.cpuBursts[0]):
                if(self.ID < other.ID):
                    return True       
            return False
        else:
            return False
   

    def __lt__(self,other):
        if(self.mode == 0):
            if (self.arrTime < other.arrTime):
                return True
            elif(self.arrTime == other.arrTime):
                if(self.ID > other.ID):
                    return True
            return False
        elif(self.mode == 1):
            if (self.CPU_bursts[0] < other.CPU_bursts[0]):
                return True
            elif(self.CPU_bursts[0] == other.CPU_bursts[0]):
                if(self.ID > other.ID):
                    return True
            return False
        elif(self.mode == 2):
            if (self.Prio < other.Prio):
                return True
            elif(self.Prio == other.Prio):
                if(self.ID > other.ID):
                    return True
            return False
        elif(self.mode == 3):
            if (self.CPU_bursts[0] < other.CPU_bursts[0]):
                return True
            elif(self.CPU_bursts[0] == other.CPU_bursts[0]):
                if(self.ID > other.ID):
                    return True
            return False
        else:
            return False