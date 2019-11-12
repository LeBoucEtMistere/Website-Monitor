from monitor import Monitor
from stats import Stats
from display import StatDisplay
from alert import Alert


class Pipeline:
    """A class that let the user easily create multiple monitoring pipelines in a modular way."""

    def __init__(self, url, monitoring_interval):
        """ Constructor of the class.

        Parameters:
            url (str): The string representing the url of the website to monitor. 

        """
        self.url = url
        self.monitoring_interval = monitoring_interval
        self.stats = []
        self.tasks = []
        self.tasks.append(
            Monitor(self.url, self.monitoring_interval, self.stats))

    def add_stat(self, timeframe, should_display, display_interval, should_alert):
        """ Add a stat object to the pipelien to hold data over a specific time period.
        It lets the user display it at a regular rate and enable alerts for this timeframe.

        Parameters:
            timeframe (int): The timeframe over which the stats should be computed. in seconds
            should_display (bool): A boolean that enables the displaying for these stats.
            display_interval (int): The interval in seconds there should be between each diplay of the stats
            should_alert (bool): A boolean that enables the alerting for these stats, over the same timeframe.

        """
        self.stats.append(Stats(timeframe))
        if should_display:
            self.tasks.append(StatDisplay(
                self.url, self.stats[-1], display_interval))
        if should_alert:
            self.tasks.append(
                Alert(self.stats[-1], self.monitoring_interval, self.url))

    def run(self, executor):
        """ Submit every tasks of the pipeline, starting with the monitor, to the executor passed as argument.

        Parameters:
            executor (concurrent.futures.Executor): The executor used to start the tasks

        """
        print("Launching pipeline for website {}".format(self.url))
        for t in self.tasks:
            executor.submit(t.run)

    def stop(self):
        """ Stop every tasks in the pipeline."""
        print("Stopping pipeline for website {}".format(self.url))
        for t in self.tasks:
            t.stop()
