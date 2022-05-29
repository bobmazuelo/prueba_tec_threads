#!/bin/python3

#import threading
import multiprocessing as mp
import queue
import time
import random
import argparse

class Productor(mp.Process):
    def __init__(self, queue, lock):
        self.queue = queue
        self.lock = lock
    
    def run(self):
        while True:
            self.lock.acquire()
            try:
                if (self.queue.full()):
                    self.lock.wait()
                self.queue.put(random.random())
                time.sleep(0.01)
            finally:
                self.lock.release()
                return self.queue

class Consumidor(mp.Process):
    def __init__(self, queue, lock, funct):
        self.queue = queue
        self.lock = lock
        self.funct = funct

    def run(self):
        while True:
            self.lock.acquire()
            try:
                if (self.queue.empty()):
                    self.lock.wait()
                item = self.queue.get()
            finally:
                self.lock.release()
                return self.funct(item)

def printed(name):
    print(str(name))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("processes", type=int)
    n_processes = parser.parse_args().processes
    
    q = queue.Queue(maxsize=5)
    lock = mp.Lock()
    processes_prod = []
    processes_cons = []

    for _ in range(n_processes):
        p = mp.Process(name="Producer", target=Productor, args=(q, lock,))
        c = mp.Process(name="Consumer", target=Consumidor, args=(q, lock, printed,))
        processes_prod.append(p)
        processes_cons.append(c)

    for p, c in zip(processes_prod, processes_cons):
        p.start()
        c.start()

    for p, c in zip(processes_prod, processes_cons):
        p.join()
        c.join()

if __name__ == "__main__":
    main()
