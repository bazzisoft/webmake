"""
A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages, Command
from setuptools.command.install import install as setuptools_install
from setuptools.command.develop import develop as setuptools_develop

# To use a consistent encoding
from codecs import open
from os import path
import os
import sys
import subprocess

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    from setuptools.command.install import install as bdist_wheel


here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    contents = f.read()
    short_description = contents.splitlines()[2]
    long_description = "\n".join(contents.splitlines()[2:]).split("----------")[0]


# Ensure required packages are installed
def program_is_installed(msg, prog):
    try:
        sys.stdout.write(msg)
        sys.stdout.flush()
        subprocess.check_call(prog, shell=True)
    except:
        return False
    return True


if not program_is_installed(
    "Detecting nodejs...", "node -v"
) or not program_is_installed("Detecting npm...", "npm -v"):
    sys.stderr.write("\n" + "-" * 79)
    sys.stderr.write(
        "\nERROR: webmake requires `node` and `npm` to be available prior to installation."
    )
    sys.stderr.write("\n" + "-" * 79 + "\n\n")
    raise Exception(
        "webmake requires `node` and `npm` to be available prior to installation."
    )


# Setup post install script
def _post_install(dir):
    oldwd = os.getcwd()
    os.chdir(dir)
    os.system("npm install --color false --unicode false")
    os.chdir(oldwd)


class CustomInstall(setuptools_install):
    def run(self):
        setuptools_install.run(self)
        self.execute(
            _post_install,
            (os.path.join(self.install_lib, "webmake"),),
            msg="Installing NPM dependencies",
        )


class CustomDevelop(setuptools_develop):
    def run(self):
        setuptools_develop.run(self)
        self.execute(
            _post_install,
            (os.path.join(self.dist.location, "webmake"),),
            msg="Installing NPM dependencies",
        )


# PIP setup function
setup(
    # Custom install command classes
    cmdclass={
        "install": CustomInstall,
        "develop": CustomDevelop,
    },
    # Project name,
    name="webmake",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="4.1.2",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="https://github.com/bazzisoft/webmake",
    # Author details
    author="Barak Shohat",
    author_email="barak@bazzisoft.com",
    # Choose your license
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    # What does your project relate to?
    keywords="make makefile build tool packaging web javascript less sass",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    packages=find_packages(exclude=("dist", "tests", "node_modules")),
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "watchdog>=0.8",
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        #'dev': ['pylint'],
        #'test': [],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        "webmake": ["package.json", "cordova/hooks/before_prepare/runwebmake.py"],
    },
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        "console_scripts": [
            "webmk=webmake.main:main",
        ],
    },
)
