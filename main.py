import validators
from monitor import Monitor
from stats import Stats
from display import StatDisplay
from alert import Alert
from pipeline import Pipeline
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

    print("Website monitoring tool")
    url = input("please enter the url of the website you want to monitor: ")
    if not validators.url(url) and not validators.domain(url):
        print("Url entered is not a valid url or doamin name. Exiting the program.")
        return
    if not validators.url(url):
        url = 'http://' + url
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

    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    try:
        p = Pipeline(url, interval)
        p.add_stat(120, 10, True)
        p.add_stat(600, 60, False)

        p.run()

    except ServiceExit:
        p.stop()

    print("Goodbye !")


if __name__ == "__main__":
    main()
