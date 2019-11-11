import validators
from pipeline import Pipeline
import signal
import argparse


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

    parser = argparse.ArgumentParser(prog='main.py',
                                     usage='%(prog)s [options] websites',
                                     description='Monitor a given website at a given frequency and prints useful stats about it.')

    parser.add_argument('websites',
                        metavar='websites',
                        type=str,
                        help='a list of websites separated by commas')
    parser.add_argument('-i',
                        '--interval',
                        help='the interval in seconds at which the sites must be monitored',
                        nargs='?', const=1, type=int)
    args = parser.parse_args()
    print(args)

    urls = args.websites.split(',')
    interval = int(args.interval)

    if interval <= 0:
        print('Invalid negative or null interval time used')
        return

    for url in urls:

        if not validators.url(url) and not validators.domain(url):
            print(
                "Url entered is not a valid url or domain name ({}). Exiting the program.".format(url))
            return
        if not validators.url(url):
            url = 'http://' + url

    print(urls)
    print(interval)

    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    print("Starting the monitoring process, press CTRL+C to exit program.")
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
