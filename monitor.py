import requests
from time import time
from task import Task


class Monitor(Task):
    """ A class that holds the monitoring logic for a given website."""

    def __init__(self, url, periodicity, stats_list):
        """ The constructor of the class

        Parameters:
            url (str): The url of the website to monitor.
            periodicity (int): The period at which the monitoring should happen, in seconds.
            stats_list (list<Stats>): a list of stats object to feed with the data from the monitoring.
        """
        super().__init__(periodicity)
        self.url = url
        self.stats_list = stats_list

    def do_work(self):
        """ The core logic of the monitoring class. """
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
            # if the website is not reachable or returned an error code above 500.
            data["timestamp"] = time()
            data["request_success"] = False

        for stat in self.stats_list:
            stat.add_data(data)
