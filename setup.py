#!/usr/bin/env python
import io
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from distutils.util import convert_path


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["--cov", ".", "--cov-config", ".coveragerc"]
        self.test_suite = True

    def run_tests(self):
        import pytest

        sys.exit(pytest.main(self.test_args))


PROJECT = "arena-cli"
package_config = {}
version_file_path = convert_path("arena/version.py")

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open(version_file_path) as version_file:
    exec(version_file.read(), package_config)

tests_require = [
    "coverage==4.5.4",
    "coveralls==1.3.0",
    "flake8==3.0.4",
    "pytest==3.5.1",
    "pytest-cov==2.5.1",
    "pytest-env==0.6.2",
    "responses==0.9.0",
    "pre-commit==1.14.4",
]

setup(
    name=PROJECT,
    cmdclass={"test": PyTest},
    version=package_config["__version__"],
    description="Use Arena through command line interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="synkrotron",
    author_email="",
    url="https://www.synkrotron.ai",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
    platforms=["Any"],
    install_requires=requirements,
    tests_require=tests_require,
    packages=find_packages(exclude=("docs", "scripts", "tests")),
    include_package_data=True,
    entry_points={'console_scripts': ['arena=arena.main:main']},
    zip_safe=False,
)
