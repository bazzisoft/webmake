import os
import sys
import argparse
import importlib
import functools
import traceback
from .modules import utils
from . import settings, compiler, watcher


def command_line_error(parser, makefile, message):
    tb = sys.exc_info()[2]
    lineinfo = ''
    if tb:
        try:
            tb = [s for s in reversed(traceback.extract_tb(tb)) if s[0].endswith('webmakefile.py')][0]
            lineinfo = 'webmakefile.py:{}: '.format(tb[1])
        except IndexError:
            pass

    msg = '\nProcessing: {}\n\n{}{}'.format(makefile, lineinfo, message)
    parser.error(msg)


def parse_command_line():
    default_webmakefile = os.path.join(os.getcwd(), 'webmakefile.py')

    parser = argparse.ArgumentParser(description='A simple pythonic build system for Web and Cordova projects (JS,Less,Sass...)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')
    parser.add_argument('-r', '--release', action='store_true', help='Release mode. Minify output and don\'t generate source maps.')
    parser.add_argument('-f', '--force', action='store_true', help='Force recompilation of all source files, even if not modified.')
    parser.add_argument('-m', '--makefile', default=default_webmakefile, help='Specify the webmakefile.py to use for compilation settings.')
    parser.add_argument('-w', '--watch', action='store_true', help='Watch all input files for changes, and recompile automatically.')
    parser.add_argument('-p', '--polling-watcher', action='store_true', help='Use the polling watcher instead of inotify (increased compatibility).')

    args = parser.parse_args()
    error_fn = functools.partial(command_line_error, parser, args.makefile)

    if not args.makefile or not os.path.isfile(args.makefile):
        error_fn('webmakefile.py does not exist, please create one in '
                 'your project root and run from there.')

    return (args, error_fn)


def main():
    args, error_fn = parse_command_line()
    settings.VERBOSE = args.verbose
    settings.RELEASE = args.release
    settings.FORCE = args.force
    settings.MAKEFILEPATH = args.makefile

    webmakefile_dir = os.path.abspath(os.path.expanduser(os.path.dirname(args.makefile)))
    webmakefile_name = os.path.basename(args.makefile)
    webmakefile_module = os.path.splitext(webmakefile_name)[0]

    os.chdir(webmakefile_dir)
    sys.path.insert(0, webmakefile_dir)

    try:
        makefile = importlib.import_module(webmakefile_module)
    except RuntimeError as e:
        error_fn(str(e))
    except Exception as e:  # pylint: disable=broad-except
        error_fn('Unable to parse webmakefile.py.\n\n{}'.format(str(e)))

    try:
        settings.MAKEFILE = makefile.MAKEFILE
    except AttributeError:
        error_fn('MAKEFILE variable missing in webmakefile.py.')

    utils.logv('WEBMAKEFILE = {}', os.path.join(webmakefile_dir, webmakefile_name))
    utils.logv('RELEASE MODE = {}', ('On' if settings.RELEASE else 'Off'))
    utils.logv('FORCE COMPILATION = {}', ('On' if settings.FORCE else 'Off'))

    # Load any cached dependencies
    compiler.load_dependencies_from_cache(settings.MAKEFILE, settings.MAKEFILEPATH)

    if settings.FORCE:
        if not compiler.compile_all(settings.MAKEFILE, settings.MAKEFILEPATH, settings.RELEASE):
            sys.exit(1)
    else:
        if not compiler.compile_if_modified(settings.MAKEFILE, settings.MAKEFILEPATH, release=settings.RELEASE):
            sys.exit(1)

    if args.watch:
        watcher.start_watching(use_polling_watcher=args.polling_watcher)
