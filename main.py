import validators
from monitor import Monitor
from stats import StatDisplay, Stats
from concurrent.futures import ThreadPoolExecutor
import signal


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    print(' Closing application properly ...')
    raise ServiceExit


def main():

    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    print("Website monitoring tool")
    url = input("please enter the url of the website you want to monitor: ")
    if not validators.url(url):
        print("Url entered is not a valid url. Exiting the program.")
        return
    interval = input("please enter the checking interval in seconds: ")
    try:
        interval = int(interval)
        assert(interval > 0)
    except ValueError:
        print("The input is not a valid integer. Exiting the program. ")
        return
    except AssertionError:
        print("The input is not a strictly positive integer. Exiting the program. ")
        return

    stat2m = Stats(120)
    stat10m = Stats(600)
    monitors = []
    monitors.append(Monitor(url, interval,  [stat2m, stat10m]))
    consumers = []
    consumers.append(StatDisplay(stat2m, 10))
    consumers.append(StatDisplay(stat10m, 60))

    try:
        with ThreadPoolExecutor() as executor:
            for m in monitors:
                executor.submit(m.start)
            for c in consumers:
                executor.submit(c.display)

    except ServiceExit:
        for m in monitors:
            m.stop()
        for c in consumers:
            c.stop()

    print("Goodbye !")


if __name__ == "__main__":
    main()
