from time import time, sleep
from threading import Event


class Task:
    """ A generic class used to represent a threaded task that repeat every period and can be stopped."""

    def __init__(self, period):
        """ The constructor of the class

        Parameters:
            period (int): The period in seconds of the task.
        """
        self.stopping = Event()
        self.period = period

    def stop(self):
        """ A method that stops the main loop of the task and allow the thread to join."""
        self.stopping.set()

    def run(self):
        """ The main loop of the task, execute the code logic in the method do_work() that should be defined by child classes."""
        origin_time = time()
        while not self.stopping.is_set():
            if time() - origin_time > self.period:
                origin_time = time()
                self.do_work()
            else:
                sleep(0.1)

    def do_work(self):
        """ The method that implements the task logic, should be redefined by children classes."""
        raise NotImplementedError
