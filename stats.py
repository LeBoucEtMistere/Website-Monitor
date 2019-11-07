import threading
from time import time, sleep
from collections import Counter


class StatDisplay:
    def __init__(self, stat_provider, delay):
        self.stat_provider = stat_provider
        self.stopping = threading.Event()
        self.delay = delay

    def stop(self):
        self.stopping.set()

    def display(self):
        origin_time = time()
        while not self.stopping.is_set():
            if time() - origin_time > self.delay:
                origin_time = time()
                result = self.stat_provider.get_stats()
                if not result is None:
                    print('Over timeframe of {}s, availability = {:.1f}%, max response time = {:.3f}s, avg response time = {:.3f}s, codes count = {}'.format(
                        *result))
            else:
                sleep(0.1)
        return None


class Stats:
    def __init__(self, timeframe):
        self.timeframe = timeframe
        self.lock = threading.Lock()
        self.data = []

    def _compute_stats(self):
        t = time()
        recent_data = []

        self.lock.acquire()
        timeframe = self.timeframe

        if len(self.data) == 0:
            return None

        for d in self.data:
            if t - d["timestamp"] < self.timeframe:
                recent_data.append(d)
        self.data = recent_data
        self.lock.release()

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

    def add_data(self, data):
        self.lock.acquire()
        self.data.append(data)
        self.lock.release()
