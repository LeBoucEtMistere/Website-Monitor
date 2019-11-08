from time import time, sleep
from threading import Event


class Task:
    def __init__(self, period):
        self.stopping = Event()
        self.period = period

    def stop(self):
        self.stopping.set()

    def run(self):
        origin_time = time()
        while not self.stopping.is_set():
            if time() - origin_time > self.period:
                origin_time = time()
                self.do_work()
            else:
                sleep(0.1)

    def do_work(self):
        raise NotImplementedError
