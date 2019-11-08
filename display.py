from task import Task


class StatDisplay(Task):
    def __init__(self, stat_provider, delay):
        super().__init__(delay)
        self.stat_provider = stat_provider

    def do_work(self):
        result = self.stat_provider.get_stats()
        if not result is None:
            print('Over timeframe of {}s, availability = {:.1f}%, max response time = {:.3f}s, avg response time = {:.3f}s, codes count = {}'.format(
                *result))
