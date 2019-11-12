import validators
from pipeline import Pipeline
import signal
import argparse
from concurrent.futures import ThreadPoolExecutor


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
    # Create a parser for the arguments and defining them
    parser = argparse.ArgumentParser(prog='main.py',
                                     usage='%(prog)s [options] websites',
                                     description='Monitor a given website at a given frequency and prints useful stats about it.')

    parser.add_argument('websites',
                        metavar='websites',
                        type=str,
                        help='a list of websites separated by commas')
    parser.add_argument('-i',
                        '--interval',
                        help='the interval in seconds at which the sites must be monitored, default is 1 second',
                        nargs='?', const=1, type=int)

    # Parse the args
    args = parser.parse_args()
    urls = args.websites.split(',')

    # Check if args are well formated
    if args.interval is None:
        interval = 1
    else:
        interval = int(args.interval)

    if interval <= 0:
        print('Invalid negative or null interval time used')
        return

    for i in range(len(urls)):

        if not validators.url(urls[i]) and not validators.domain(urls[i]):
            print(
                "Url entered is not a valid url or domain name ({}). Exiting the program.".format(urls[i]))
            return
        if not validators.url(urls[i]):
            urls[i] = 'http://' + urls[i]

    # redirect SIGTERM and SIGINT signals to stop program
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    pipelines = []
    print("Starting the monitoring process, press CTRL+C to exit program.")
    try:
        with ThreadPoolExecutor() as executor:
            for url in urls:
                # Create a pipeline for each url and start it
                p = Pipeline(url, interval)
                # A stat that won't be displayed but that will alert
                p.add_stat(120, False, 0, True)
                # Two stats that will be displayed and won't alert
                p.add_stat(600, True, 10, False)
                p.add_stat(3600, True, 60, False)

                p.run(executor)
                pipelines.append(p)

    # catch SIGTERM and SIGINT signals to stop program properly
    except ServiceExit:
        for p in pipelines:
            p.stop()

    print("Goodbye !")


if __name__ == "__main__":
    main()
