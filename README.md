# Website-Monitor
A PoC website monitor

# How to execute
This project is coded in python and ready to be installed in a virtual env.
To begin, create a virtual env and install the dependencies:
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

To launch the program, just activate the virtual env and start the main script
```bash
source env/bin/activate
python main.py -i 1 google.com
```

To deactivate the virtual env:
```bash
deactivate
```

# Improvements for this application design

The first major improvement that I would made would be to switch from python to a language that is more fitted to multithreading performances.
The choice of python in the first place is motivated by the short period of time I had to develop this project and that it is at this time the language I am the most familiar and fluent with.
But it has several limitations. Even tough its modern library ```concurrent.futures``` that brings it on par with java regarding multiprocessing and multithreading from a syntaxic point of view, the performances are not has good, mainly because of the restrictions of the CPython implementation linked to the GIL. 
That said, as most of the program is not CPU intensive but waiting for I/O, that performance difference is not as important and comforted my choice of language for a first iteration.
In order to solve that issue, I would turn to a more system-friendly language as Rust or Go. I used Rust a bit and was impressed with the ease it has to deal with threaded programs and avoid by design data races and deadlocks. Had I been more fluent with Rust, I think I would have used it for this project.

Another step would be to had even more modularity in the code. I wanted to be as modular as possible so I implemented the concept of pipelines where many tasks cohabit and operate on the same data. Currently, the pipeline can be composed of a monitor, the corner stone that polls websites and create data points, a display that prints statistics in the console at regular intervals, and an alert that monitors the state of the availability statistics over a particular timeframe.
This pipeline structures already allows the program to easily monitor multiple websites at the same time.
One could improve this system and extend its functionnalities simply by adding new tasks to the pipeline. Examples could be:
- a task that saves datapoints in a local database, e.g. sqlite.
- a task that sends statistics over the network to another service, or a network database.
- a task that sends a notification mail to an user when an alert triggers.
etc.

The design I choosed make these additions easy as the developper only needs to derive another child class from the class Task.
Currently, the only statistic that is monitored is the availability, but the Alert class could be modified to allow the user to choose which statistics he wants to be monitored and alerted precisely.

A last improvement that could be made would be to improve the display. Actually there is a lot that can be done to improve this. The use of a console library such as ncurses would allow the program to persist alert on the display and only show the latest statistics, without the need for the user to scroll. It would also enable the use of keyboards events, and let the user use keys to pause the monitoring for instance, or show a particular stat on a particular website. The top thing would be to add a graphic display of the stats, like a plot of the availability timeseries or an histogram of the status_code counts.

