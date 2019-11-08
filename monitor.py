import requests
from time import time
from task import Task


class Monitor(Task):
    def __init__(self, url, periodicity, stats_list):
        super().__init__(periodicity)
        self.url = url
        self.stats_list = stats_list

    def do_work(self):
        data = {}
        try:
            response = requests.get(
                self.url, timeout=(self.period, 30))
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
