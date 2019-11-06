import threading


class StatConsumer:
    def __init__(self, queue):
        self.queue = queue
        self.stopping = threading.Event()

    def stop(self):
        self.stopping.set()

    def consume(self):
        while not self.stopping.is_set():
            try:
                data = self.queue.get(timeout=.1)
                print(data)
            except:
                pass
        return None
