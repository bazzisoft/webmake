Webmake
=======
A simple pythonic build system for Web and Cordova projects (JS, Less, Sass...)

- Python alternative to ``grunt`` or ``gulp``.
- Supports Python 2.7 or 3.2+.
- Builds based on a ``webmakefile.py`` script in your project root.
- Can be used from the command line, on demand or in "watch for changes" mode.
- Middleware plugin for use with Django.
- Build hook for use with Cordova.
- Currently supports:
    - Browserify (vendor libs, user libs, project-specific sources)
    - React.js JSX compilation
    - LESS compilation
    - Sass compilation
    - Minification
    - Copy assets (images, fonts, etc)
    - Concatenation
    - Debug mode to generate source maps


----------


Installation
============

1. Ensure you have `node.js <https://nodejs.org/en/>`_ and ``npm`` installed.

2. Install from PyPI::

        pip install webmake

   Or directly from git::

        pip install -e git+https://github.com/bazzisoft/webmake.git@master#egg=webmake

3. Run from the command line::

        webmk -h


Usage
=====

**TBD**:

- Makefile format
- Command line invocation
- Cordova integration
- Django integration
- Force release mode in deployment process
- Test/example project


Webmake Development
===================

Todo List
---------
- Write usage documentation.
- Create proper test project.


Development Installs
--------------------
1. Create a Python 2.7 or Python 3 virtualenv.
2. For a development (--editable) install (where webmake is editable in place)::

        pip install -e /path/to/webmake

   or::

        pip install -e git+https://github.com/bazzisoft/webmake.git@master#egg=webmake

3. To test a production installation::

        pip install /path/to/webmake


PyPI Releases
-------------
1. Update version number in ``setup.py``.
2. Start Python3 virtualenv from ``tests\test_project\venv``.
3. Create a package to test with::

        python setup.py sdist

4. If first release, register on test site::

        python setup.py register -r pypitest

5. Build & submit new release::

        python setup.py sdist upload -r pypitest

6. If first release, register on live site::

        python setup.py register -r pypi

7. Build & submit new release::

        python setup.py sdist upload -r pypi
