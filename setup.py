#!/usr/bin/env python
# $ pip install twine setuptools wheel

import io
from os import system as bash, path
from sys import exit
from sys import executable
from shutil import rmtree
from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'pidtuning'
DESCRIPTION = 'PID tuning server for factorial order models.'
URL = 'https://github.com/jeancahu/PID_synthesis_wheel_package'
EMAIL = 'jeancahu@gmail.com'
AUTHOR = 'Jeancarlo Hidalgo'
REQUIRES_PYTHON = '>=3.6.0'

# What packages are required for this module to be executed?
REQUIRED = [
    'numpy',
    'Django',
    'sympy==1.5.1',
    'pandas',
]

# What packages are optional?
EXTRAS = {
}

here = path.abspath(path.dirname(__file__))

try:
    with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
with open(path.join(here, "src/pidtuning", '__version__.py')) as f:
    exec(f.read(), about)

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        bash('{0} setup.py sdist bdist_wheel --universal'.format(executable))

        self.status('Uploading the package to PyPI via Twine…')
        bash('twine upload dist/*')

        self.status('Pushing git tags…')
        bash('git tag v{0}'.format(about['__version__']))
        bash('git push --tags')

        exit()

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='GPLv3',
    classifiers=[
        # Trove classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
