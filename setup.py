import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "yoga",
    version = "0.1",
    author = "Micah Nordland",
    author_email = "micah-yoga@rehack.me",
    description = ("A flexible command line like argument parser"),
    license = "MIT",
    keywords = "argument parsing ",
    packages=['yoga', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Shells",
    ],
)
