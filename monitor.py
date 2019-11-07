import requests
from time import sleep, time
import threading


class Monitor:
    def __init__(self, url, interval, stats_list):
        self.url = url
        self.interval = interval
        self.stats_list = stats_list
        self.stopping = threading.Event()

    def stop(self):
        self.stopping.set()

    def start(self):
        origin_time = time()
        while not self.stopping.is_set():
            if time() - origin_time > self.interval:
                origin_time = time()

                data = {}
                try:
                    response = requests.get(
                        self.url, timeout=(self.interval, 30))
                    response.raise_for_status()
                    data["timestamp"] = time()
                    data["request_success"] = True
                    data["status_code"] = response.status_code
                    data["response"] = response

                except requests.exceptions.RequestException:
                    data["timestamp"] = time()
                    data["request_success"] = False

                for stat in self.stats_list:
                    stat.add_data(data)
            else:
                sleep(0.01)
        return None
