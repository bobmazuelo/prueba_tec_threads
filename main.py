import threading
import queue
import time
import random
import argparse

class Productor(threading.Thread):
    def __init__(self, queue, lock,):
        self.queue = queue
        self.lock = lock
    
    def run(self):
        while True:
            self.lock.acquire()
            try:
                self.queue.put(random.random())
                time.sleep(0.01)
            finally:
                self.lock.release()
                return self.queue

class Consumidor(threading.Thread):
    def __init__(self, queue, lock, funct):
        self.queue = queue
        self.lock = lock
        self.funct = funct
    def run(self):
        while True:
            try:
                item = self.queue.get()
                return self.funct(item)
            finally:
                self.wait()

def printed(name):
    print(str(name))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("threads", type=int)
    n_processes = parser.parse_args().threads
    
    q = queue.Queue(maxsize=5)
    lock = threading.Lock()
    processes_prod = []
    processes_cons = []

    for _ in range(n_processes):
        p = threading.Thread(target=Productor, args=(q, lock,))
        processes_prod.append(p)

    for _ in range(n_processes):
        c = threading.Thread(target=Consumidor, args=(q, lock, printed,))
        processes_cons.append(c)

    
    for p, c in zip(processes_prod, processes_cons):
        p.start()
        c.start()

    for p, c in zip(processes_prod, processes_cons):
        p.join()
        c.join()

if __name__ == "__main__":
    main()
