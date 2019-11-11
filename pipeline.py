from monitor import Monitor
from stats import Stats
from display import StatDisplay
from alert import Alert


class Pipeline:
    def __init__(self, url, monitoring_interval):
        self.url = url
        self.monitoring_interval = monitoring_interval
        self.stats = []
        self.tasks = []
        self.tasks.append(
            Monitor(self.url, self.monitoring_interval, self.stats))

    def add_stat(self, timeframe, display_interval, should_alert):
        self.stats.append(Stats(timeframe))
        self.tasks.append(StatDisplay(
            self.url, self.stats[-1], display_interval))
        if should_alert:
            self.tasks.append(
                Alert(self.stats[-1], self.monitoring_interval, self.url))

    def run(self, executor):
        print("Launching pipeline for website {}".format(self.url))
        for t in self.tasks:
            executor.submit(t.run)

    def stop(self):
        print("Stopping pipeline for website {}".format(self.url))
        for t in self.tasks:
            t.stop()
