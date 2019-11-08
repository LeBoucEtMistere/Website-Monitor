from task import Task
from datetime import datetime


class Alert(Task):
    def __init__(self, stat_provider, periodicity, website):
        super().__init__(periodicity)
        self.stat_provider = stat_provider
        self.website = website
        self.flag_alert = False

    def do_work(self):
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
