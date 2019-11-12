from task import Task


class StatDisplay(Task):
    """ A class that holds the stats display logic for a given stats object."""

    def __init__(self, website, stat_provider, delay):
        """ Constructor of the class.

        Parameters:
            website (str): The description of the website, usually its url, for display purposes.
            stat_provider (Stats): The stats object on which the display should work.
            delay (int): The time period in seconds at which the task should repeat.

        """
        super().__init__(delay)
        self.website = website
        self.stat_provider = stat_provider

    def do_work(self):
        """ Core logic of the display task that is repeated every period."""
        result = self.stat_provider.get_stats()
        if not result is None:
            print('[{}] Over timeframe of {}s, availability = {:.1f}%, max response time = {:.3f}s, avg response time = {:.3f}s, codes count = {}'.format(
                self.website, *result))
