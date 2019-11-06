import requests
from time import sleep
import threading


class Monitor:
    def __init__(self, url, interval, queue):
        self.url = url
        self.interval = interval
        self.queue = queue
        self.stopping = threading.Event()

    def stop(self):
        self.stopping.set()

    def start(self):
        while not self.stopping.is_set():
            data = {}
            try:
                response = requests.get(self.url)
                data["request_success"] = True
                data["status_code"] = response.status_code

            except requests.exceptions.RequestException:
                data["request_success"] = False

            self.queue.put(data)
            sleep(self.interval)
        return None
