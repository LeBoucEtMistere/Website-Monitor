import validators
from monitor import Monitor
from stats import StatConsumer
from concurrent.futures import ThreadPoolExecutor, wait
import queue
import signal
import time


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    print('Closing application properly ...')
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

    pipeline = queue.Queue()

    monitors = []
    monitors.append(Monitor(url, interval,  pipeline))
    consumers = []
    consumers.append(StatConsumer(pipeline))

    with ThreadPoolExecutor(max_workers=4) as executor:
        try:
            executor.submit(monitors[0].start)
            executor.submit(consumers[0].consume)
            while True:
                time.sleep(.5)

        except ServiceExit:
            monitors[0].stop()
            consumers[0].stop()

    print("Goodbye !")


if __name__ == "__main__":
    main()
