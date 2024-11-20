import itertools
import os
import signal
import time
import threading

from watchdog import events
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from . import compiler, settings
from .modules.utils import log


DEBOUNCE_DELAY = 0.3


class WatchdogEventHandler(FileSystemEventHandler):
    def __init__(self, signal_exit):
        self.signal_exit = signal_exit
        self.timer = None

    def on_any_event(self, event):
        if (
            event.is_directory
            or event.src_path.endswith(".depscache")
            or event.event_type
            in (
                events.EVENT_TYPE_OPENED,
                events.EVENT_TYPE_CLOSED,
                events.EVENT_TYPE_CLOSED_NO_WRITE,
            )
        ):
            return

        if os.path.abspath(event.src_path) == os.path.abspath(settings.MAKEFILEPATH):
            log(
                "Detected change to makefile {}, please restart the watcher.\n".format(
                    settings.MAKEFILEPATH
                )
            )
            self.signal_exit()
            return

        what = "directory" if event.is_directory else "file"
        log("{} {} {}".format(event.event_type.title(), what, event.src_path))

        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(DEBOUNCE_DELAY, self.on_timer)
        self.timer.start()

    def on_timer(self):
        compiler.compile_if_modified(
            settings.MAKEFILE, settings.MAKEFILEPATH, settings.RELEASE
        )
        log("Build complete.\n")


def start_watching(use_polling_watcher=False):
    settings.VERBOSE = True

    paths = itertools.chain.from_iterable(d["dependencies"] for d in settings.MAKEFILE)
    paths = set(os.path.abspath(os.path.dirname(p)) for p in paths)

    # import pprint
    # pprint.pprint(paths, indent=4)

    # Use the polling observer instead of inotify if polling was requested
    if use_polling_watcher:
        log("\nWatching for filesystem changes (polling watcher), Ctrl-C to exit...\n")
        observer = PollingObserver(timeout=3)
    else:
        log("\nWatching for filesystem changes, Ctrl-C to exit...\n")
        observer = Observer()

    shutdown = False

    def signal_exit(sig=None, frame=None):
        log("Shutting down...")
        observer.stop()
        nonlocal shutdown
        shutdown = True

    for path in paths:
        observer.schedule(WatchdogEventHandler(signal_exit), path, recursive=False)
    observer.start()

    signal.signal(signal.SIGINT, signal_exit)
    signal.signal(signal.SIGTERM, signal_exit)

    try:
        while not shutdown:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    observer.join()
