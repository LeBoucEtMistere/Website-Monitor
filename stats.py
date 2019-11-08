from threading import Lock
from time import time
from collections import Counter


class Stats:
    def __init__(self, timeframe):
        self.timeframe = timeframe
        self.lock = Lock()
        self.data = []

    def _get_data_in_timeframe(self):
        t = time()
        recent_data = []

        with self.lock:
            timeframe = self.timeframe

            if len(self.data) == 0:
                return None

            for d in self.data:
                if t - d["timestamp"] < self.timeframe:
                    recent_data.append(d)
            self.data = recent_data

        return recent_data

    def _compute_stats(self):
        t = time()
        recent_data = []

        with self.lock:
            timeframe = self.timeframe

            if len(self.data) == 0:
                return None

            for d in self.data:
                if t - d["timestamp"] < self.timeframe:
                    recent_data.append(d)
            self.data = recent_data

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
            return timeframe, 0., 0., 0., None

        return timeframe, availability * 100 / len(recent_data), max(response_times), sum(response_times)/len(response_times), Counter(codes)

    def get_stats(self):
        return self._compute_stats()

    def get_availability(self):
        t = time()
        recent_data = []
        with self.lock:
            timeframe = self.timeframe

            if len(self.data) == 0:
                return None

            for d in self.data:
                if t - d["timestamp"] < self.timeframe:
                    recent_data.append(d)
            self.data = recent_data

        availability = 0
        for d in recent_data:
            if d["request_success"] and d["status_code"] < 500:
                availability += 1
        return availability * 100 / len(recent_data)

    def add_data(self, data):
        with self.lock:
            self.data.append(data)
