"""
Middleware class to watch dependencies and automatically
compile static files during development.

Usage
-----

1. Add the following to your local/development settings::

        # Webmake Middleware
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
            'webmake.django.middleware.WebmakeCompilerMiddleware',
        )

2. Create a ``webmakefile.py`` in your project root, and add the
files to compile.

3. Call ``webmk -fr`` from your deployment process to create
release versions of all target files::

        def pre_process(self, deployment_settings, *args, **kwargs):
            with lcd(PROJECT_PATH):
                local('webmk -fr')
"""
import re
import os
import sys
import subprocess
import warnings
from django.conf import settings  # pylint: disable=import-error


SETTINGS_ROOT = os.path.dirname(os.path.abspath(os.path.join(sys.modules[settings.SETTINGS_MODULE].__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(re.sub(r'settings[/\\]?$', '', SETTINGS_ROOT), os.pardir))
WEBMAKE_BIN = 'webmk'
WEBMAKEFILE = os.path.join(PROJECT_ROOT, 'webmakefile.py')

POSSIBLE_BINFILES = [f for f in (
                         os.path.join(os.path.dirname(sys.executable), WEBMAKE_BIN),
                         os.path.join(os.path.dirname(sys.executable), WEBMAKE_BIN + '.exe'),
                     ) if os.path.isfile(f)]

BINFILE = POSSIBLE_BINFILES[0] if POSSIBLE_BINFILES else WEBMAKE_BIN


class WebmakeCompilerMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        if not settings.DEBUG:
            warnings.warn('WebmakeCompilerMiddleware should not be used in production!', RuntimeWarning)

        cmd = ' '.join([BINFILE, '-m', WEBMAKEFILE])
        env = os.environ.copy()
        env.pop('PYTHONPATH', None)

        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, env=env)
        except subprocess.CalledProcessError as e:
            output = e.output.decode('utf-8') if hasattr(e.output, 'decode') else str(e.output)
            raise RuntimeError('WebmakeCompilerMiddleware:\n' + output)

        return None
