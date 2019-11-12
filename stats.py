from threading import Lock
from time import time
from collections import Counter


class Stats:
    """ An object that holds data over a specific timeframe and computes stats on this data.
    It can be accessed from multiple threads safely. 
    """

    def __init__(self, timeframe):
        """ the constructor of the class

        Parameters:
            timeframe (int): The timeframe in seconds over which it computes the stats
        """
        self.timeframe = timeframe
        self.lock = Lock()
        self.data = []

    def _get_data_in_timeframe(self):
        """ A method that return the data points inside the timeframe and clean the internal data list from the older data points.

        Returns:
            recent_data (list<dict>): The data that falls inside the timeframe.

        """
        t = time()
        recent_data = []

        if len(self.data) == 0:
            return None

        for d in self.data:
            if t - d["timestamp"] < self.timeframe:
                recent_data.append(d)
        self.data = recent_data

        return recent_data

    def get_stats(self):
        """ A method that computes and returns the current stats over the timeframe.

        Returns:
            t (tuple): The stats including in this order: timeframe, percentage of availability, max response time, avg response time, a Counter of status_codes

        """
        with self.lock:
            recent_data = self._get_data_in_timeframe()

        availability = 0
        response_times = []
        codes = []

        for d in recent_data:
            if d["request_success"] and d["status_code"] < 500:
                availability += 1
            if d["request_success"]:
                response_times.append(
                    d["response"].elapsed.total_seconds())
                codes.append(d["status_code"])

        if availability == 0:
            return self.timeframe, 0., 0., 0., None

        return self.timeframe, availability * 100 / len(recent_data), max(response_times), sum(response_times)/len(response_times), Counter(codes)

    def get_availability(self):
        """ A method that computes and returns the current availability over the timeframe.

        Returns:
            availability (int): The percentage of availability over the timeframe.

        """
        with self.lock:
            recent_data = self._get_data_in_timeframe()
        if recent_data is None:
            return None
        availability = 0
        for d in recent_data:
            if d["request_success"] and d["status_code"] < 500:
                availability += 1
        return availability * 100 / len(recent_data)

    def add_data(self, data):
        """ A method that adds data to the stat object, in a thread safe way.

        Parameters:
            data (dict): A dictionnary representing a data point.

        """
        with self.lock:
            self.data.append(data)
