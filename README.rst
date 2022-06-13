Webmake
=======
A simple pythonic build system for Web and Cordova projects (JS, Less, Sass...)

- Python alternative to ``webpack``, ``grunt`` or ``gulp``.
- Supports Python 2.7 or 3.2+.
- Builds based on a ``webmakefile.py`` script in your project root.
- Automatically detects dependencies and builds only what's changed.
- Can be used from the command line, on demand or in "watch for changes" mode.
- Automatically generates source maps in debug mode, minifies in release mode.
- Your source code (HTML/JavaScript) stays identical whether in debug or release mode - no conditional script or CSS inclusion.
- Middleware plugin for use with Django.
- Build hook for use with Cordova.
- Currently supports:
    - Browserify (vendor libs, user libs, project-specific sources)
    - Browserify plugins: ES2015, React JSX
    - Less compilation
    - Sass compilation
    - Minification
    - Copy assets (images, fonts, etc)
    - Concatenation


----------


Installation
============

1. Ensure you have build tools, `node.js <https://nodejs.org/en/>`_ and ``npm`` installed.::

        # Ubuntu
        sudo apt-get install  build-essential nodejs npm

2. Install from PyPI::

        pip install webmake

   Or directly from git::

        pip install -e git+https://github.com/bazzisoft/webmake.git@master#egg=webmake

3. Run from the command line::

        webmk -h


Usage
=====

Sample Project
--------------

You can find a sample project in the Git repo at ``tests/test_project``.


Creating Your Makefile
----------------------

For webmake to do anything useful, you need to create a makefile in your project root directory. This should be called ``webmakefile.py``. This is a standard python module that exposes a ``MAKEFILE`` list telling webmake what to build. Here is a basic template::

    # webmakefile.py

    from webmake import api

    #
    # Arbitrary python helper functions/variables can go here
    #

    MAKEFILE = [
        # webmake API commands go here, eg:
        api.copy_files('www-dev', 'www', 'index.html'),
    ]


Command-line Invocation
-----------------------

Build in debug mode, with verbose output::

    webmake -v

Build in debug mode, and actively watch for changes::

    webmake -vw

Force a rebuild of everything in release mode (minify, no source maps)::

    webmake -fr


Webmake API
-----------

The following commands can go inside the ``MAKEFILE`` list:

Copy static assets::

    api.copy_files(src_dir='node_modules/bootstrap/fonts', dst_dir='www/fonts', filespec='*', recursive=False)

Compile LESS::

    api.compile_less(input_file='www-dev/less/base.less', output_file='www/css/base.css')

Compile Sass::

    api.compile_sass(input_file='node_modules/ratchet/sass/ratchet.scss', output_file='www/css/ratchet.css')

Browserify vendor javascript libs from ``node_modules``::

    # Top of webmakefile.py
    NODE_MODULES = ['jquery', 'underscore', 'bootstrap', 'fastclick', 'react']

    # Inside MAKEFILE list
    api.browserify_node_modules(module_name_list=NODE_MODULES, output_file='www/js/vendor.js')

Browserify user libs::

    # Usage: var Cookie = require('jslib/Cookie');
    api.browserify_libs(lib_dirs=['www-dev/jslib'], output_file='www/js/jslib.js', use_reactjs=False)

Browserify an entry point that ``require()``'s all its dependencies.
Use ``export_as=xxx`` to expose it as a ``require()``'able module named ``xxx``::

    api.browserify_file(entry_point='www-dev/js/website.js', output_file='www/js/website.js', use_reactjs=False, export_as=None)

Concatenate and compile standalone JSX files with ``react-tools``. If using browserify, use above APIs instead with ``use_reactjs=True``::

    # Top of webmakefile.py
    JSX_INPUTS = api.list_matching_files('www-dev/jsx', extensions='jsx', recursive=False)

    # Inside MAKEFILE list
    api.compile_reactjsx(input_files=JSX_INPUTS, output_file='www/js/reactjsx.js'),

Minify standalone CSS. Concatenates in debug mode, minifies in release mode::

    api.minify_css(input_files=['www-dev/less/styles.css'], output_file='www/css/styles.css')

Minify standalone JS. Concatenates in debug mode, minifies in release mode::

    api.minify_js(input_files=['www-dev/js/standalone.js'], output_file='www/js/standalone.js')

Concatenate files with no further processing::

    api.concatenate(input_files=['www-dev/js/standalone.js'] * 2, output_file='www/js/standalone-x2.js')


Django Integration
------------------

Add the built in webmake middleware to your ``MIDDLEWARE_CLASSES`` in ``DEBUG`` mode. This will automatically run ``webmk``, check for changes a recompile as necessary for each request::

    if DEBUG:
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
           'webmake.django.middleware.WebmakeCompilerMiddleware',
        )

For production, see the *Deployment Integration* section below.


Cordova Integration
-------------------

Copy the provided build hook ``webmake/cordova/hooks/before_prepare/runwebmake.py`` into your Cordova project's ``hooks`` directory, and give it executable permissions. You may need to modify the script to find your python executable.

The script will automatically invoke ``webmk -v`` or ``webmk -frv`` as part of the ``cordova prepare`` command.


Deployment Integration
----------------------

Add a step to your deployment script that calls ``webmk -fr`` to force a recompile in release mode. Then Rsync or package the files directly from your output directories.


Webmake Development
===================

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
- https://packaging.python.org/en/latest/distributing/
- http://peterdowns.com/posts/first-time-with-pypi.html

1. Update CHANGELOG.
2. Update version number in ``setup.py``.
3. Start Python3 virtualenv from ``tests/test_project/venv``.
4. Create packages to test with. Ensure both source and wheel installations work::

        python setup.py sdist
        python setup.py bdist_wheel

5. Build & submit new release on test site (source distribution only)::

        twine upload --repository-url https://test.pypi.org/legacy/ dist/webmake-x.y.z.tar.gz

6. Build & submit new release on live PyPI (source distribution only)::

        twine upload dist/webmake-x.y.z.tar.gz
