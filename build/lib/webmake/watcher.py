import os
import time
import itertools
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .modules.utils import log
from . import settings, compiler


FORCE_EXIT = False


class WatchdogEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory or event.src_path.endswith('.depscache'):
            return

        if os.path.abspath(event.src_path) == os.path.abspath(settings.MAKEFILEPATH):
            log('Detected change to makefile {}, please restart the watcher.\n'.format(settings.MAKEFILEPATH))
            global FORCE_EXIT  # pylint: disable=global-statement
            FORCE_EXIT = True
            return

        what = 'directory' if event.is_directory else 'file'
        log('{} {} {}'.format(event.event_type.title(), what, event.src_path))

        compiler.compile_if_modified(settings.MAKEFILE, settings.MAKEFILEPATH, settings.RELEASE)
        log('')


def start_watching():
    log('\nWatching for filesystem changes, Ctrl-C to exit...\n')
    settings.VERBOSE = True

    paths = itertools.chain.from_iterable(d['dependencies'] for d in settings.MAKEFILE)
    paths = set(os.path.abspath(os.path.dirname(p)) for p in paths)

#    import pprint
#    pprint.pprint(paths, indent=4)

    observer = Observer()
    for path in paths:
        observer.schedule(WatchdogEventHandler(), path, recursive=False)
    observer.start()

    try:
        while not FORCE_EXIT:
            time.sleep(1)
        raise KeyboardInterrupt()
    except KeyboardInterrupt:
        log('Shutting down...')
        observer.stop()

    observer.join()
