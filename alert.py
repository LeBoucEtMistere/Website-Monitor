from task import Task
from datetime import datetime


class Alert(Task):
    """ A class that holds the alerting logic and display for a given stats object."""

    def __init__(self, stat_provider, periodicity, website):
        """ Constructor of the class.

        Parameters:
            stat_provider (Stats): The stats object on which the alert should work.
            periodicity (int): The time period in seconds at which the task should repeat.
            website (str): The description of the website, usually its url, for display purposes.

        """
        super().__init__(periodicity)
        self.stat_provider = stat_provider
        self.website = website
        self.flag_alert = False

    def do_work(self):
        """ Core logic of the alert task that is repeated every period."""
        availability = self.stat_provider.get_availability()
        if availability is None:
            return

        if not self.flag_alert and availability < 80:
            self.flag_alert = True
            print("!!! Alert !!! Website {} is down. availability={}%, time={}".format(
                self.website, availability, datetime.now()))
        if self.flag_alert and availability >= 80:
            self.flag_alert = False
            print("!!! Alert !!! Website {} recovered. availability={}%, time={}".format(
                self.website, availability, datetime.now()))
