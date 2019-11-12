import pytest
from stats import Stats
from alert import Alert
from time import time


@pytest.fixture
def stats_good():
    s = Stats(120)
    t = time() - 120
    for i in range(120):
        data = {}
        data["timestamp"] = t + i
        data["request_success"] = True
        data["status_code"] = 200
        s.add_data(data)
    return s


@pytest.fixture
def stats_bad():
    s = Stats(120)
    t = time() - 120
    for i in range(120):
        data = {}
        data["timestamp"] = t + i
        data["request_success"] = False
        data["status_code"] = 500
        s.add_data(data)
    return s


def test_alert(stats_good, stats_bad):
    a = Alert(stats_good, 1, 'test')
    a.do_work()
    assert(a.flag_alert is False)

    b = Alert(stats_bad, 1, 'test')
    b.do_work()
    assert(b.flag_alert is True)


def test_alert_recover(stats_bad):
    b = Alert(stats_bad, 1, 'test')
    b.do_work()
    assert(b.flag_alert is True)

    t = time() - 120
    for i in range(960):
        data = {}
        data["timestamp"] = t + i/8
        data["request_success"] = True
        data["status_code"] = 200
        stats_bad.add_data(data)

    b.do_work()
    assert(b.flag_alert == False)
