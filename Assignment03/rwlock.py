from random import shuffle
from random import seed
from random import randint
#from rich import print 
import sys
#from main import *


import threading

__author__ = "Mateusz Kobos"
__source__ = "https://code.activestate.com/recipes/577803-reader-writer-lock-with-priority-for-writers/"

class RWLock:
    """Synchronization object used in a solution of so-called second 
    readers-writers problem. In this problem, many readers can simultaneously 
    access a share, and a writer has an exclusive access to this share.
    Additionally, the following constraints should be met: 
    1) no reader should be kept waiting if the share is currently opened for 
        reading unless a writer is also waiting for the share, 
    2) no writer should be kept waiting for the share longer than absolutely 
        necessary. 
    
    The implementation is based on [1, secs. 4.2.2, 4.2.6, 4.2.7] 
    with a modification -- adding an additional lock (C{self.__readers_queue})
    -- in accordance with [2].
        
    Sources:
    [1] A.B. Downey: "The little book of semaphores", Version 2.1.5, 2008
    [2] P.J. Courtois, F. Heymans, D.L. Parnas:
        "Concurrent Control with 'Readers' and 'Writers'", 
        Communications of the ACM, 1971 (via [3])
    [3] http://en.wikipedia.org/wiki/Readers-writers_problem
    """
    
    def __init__(self):
        self.__read_switch = _LightSwitch()
        self.__write_switch = _LightSwitch()
        self.__no_readers = threading.Lock()
        self.__no_writers = threading.Lock()
        self.__readers_queue = threading.Lock()
        """A lock giving an even higher priority to the writer in certain
        cases (see [2] for a discussion)"""
    
    def reader_acquire(self):
        self.__readers_queue.acquire()
        self.__no_readers.acquire()
        self.__read_switch.acquire(self.__no_writers)
        self.__no_readers.release()
        self.__readers_queue.release()
    
    def reader_release(self):
        self.__read_switch.release(self.__no_writers)
    
    def writer_acquire(self):
        self.__write_switch.acquire(self.__no_readers)
        self.__no_writers.acquire()
    
    def writer_release(self):
        self.__no_writers.release()
        self.__write_switch.release(self.__no_readers)
    

class _LightSwitch:
    """An auxiliary "light switch"-like object. The first thread turns on the 
    "switch", the last one turns it off (see [1, sec. 4.2.2] for details)."""
    def __init__(self):
        self.__counter = 0
        self.__mutex = threading.Lock()
    
    def acquire(self, lock):
        self.__mutex.acquire()
        self.__counter += 1
        if self.__counter == 1:
            lock.acquire()
        self.__mutex.release()

    def release(self, lock):
        self.__mutex.acquire()
        self.__counter -= 1
        if self.__counter == 0:
            lock.release()
        self.__mutex.release()

##
## Unit testing code
## =================
##

import threading
import time
import copy


buffer = []

class Writer(threading.Thread):
    def __init__(self, rw_lock, init_sleep_time, sleep_time, to_write):
        """
        @param buffer_: common buffer_ shared by the readers and writers
        @type buffer_: list
        @type rw_lock: L{RWLock}
        @param init_sleep_time: sleep time before doing any action
        @type init_sleep_time: C{float}
        @param sleep_time: sleep time while in critical section
        @type sleep_time: C{float}
        @param to_write: data that will be appended to the buffer
        """
        threading.Thread.__init__(self)
        self.__rw_lock = rw_lock
        self.__init_sleep_time = init_sleep_time
        self.__sleep_time = sleep_time
        self.__to_write = to_write
        self.entry_time = None
        """Time of entry to the critical section"""
        self.exit_time = None
        """Time of exit from the critical section"""
        
    def run(self):
        time.sleep(self.__init_sleep_time)
        #print("writing")
        #writer("writer_1.exe")
        self.__rw_lock.writer_acquire()
        self.entry_time = time.time()
        time.sleep(self.__sleep_time)
        buffer.append(self.__to_write)
        print(buffer)
        self.exit_time = time.time()
        self.__rw_lock.writer_release()

class Reader(threading.Thread):
    def __init__(self, rw_lock, init_sleep_time, sleep_time):
        """
        @param buffer_: common buffer shared by the readers and writers
        @type buffer_: list
        @type rw_lock: L{RWLock}
        @param init_sleep_time: sleep time before doing any action
        @type init_sleep_time: C{float}
        @param sleep_time: sleep time while in critical section
        @type sleep_time: C{float}
        """
        threading.Thread.__init__(self)
        
        self.__rw_lock = rw_lock
        self.__init_sleep_time = init_sleep_time
        self.__sleep_time = sleep_time
        self.buffer_read = None
        """a copy of a the buffer read while in critical section"""    
        self.entry_time = None
        """Time of entry to the critical section"""
        self.exit_time = None
        """Time of exit from the critical section"""

    def run(self):
        time.sleep(self.__init_sleep_time)
        print("reading")
        self.__rw_lock.reader_acquire()
        self.entry_time = time.time()
        time.sleep(self.__sleep_time)
        self.buffer_read = copy.deepcopy(buffer)
        print(buffer)
        self.exit_time = time.time()
        self.__rw_lock.reader_release()


    
if __name__=='__main__':
    
    seed(25256)

    if len(sys.argv) == 1:
        writers = 1
       
    else:
        writers = int(sys.argv[1])

    readers = int(writers) * 3
        
    rw_lock = RWLock()
    threads = []

    for i in range(writers):
        threads.append(Writer(rw_lock, 1, 0, i))

    for i in range(readers):
        threads.append(Reader(rw_lock, 0.1, 0.3))

    shuffle(threads)

    #buffer_, rw_lock, init_sleep_time, sleep_time, to_write
    threads.append(Reader(rw_lock, 0.1, 0.6))
    threads.append(Writer(rw_lock, 0.2, 0.1, 2))
    threads.append(Reader(rw_lock, 0.3, 0))
    threads.append(Reader(rw_lock, 0.4, 0))
    threads.append(Writer(rw_lock, 0.5, 0.1, 3))

    for t in threads:
        t.run()

    print(threads)

    print(buffer)
    