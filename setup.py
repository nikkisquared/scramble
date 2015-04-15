#!/usr/bin/python

from setuptools import setup

setup(
    name="scramble",
    version="1.0",
    description = "A library for scrambling streams of text.",
    url = "https://github.com/nikkisquared/scramble",
    author="Nikki",
    author_email="private",
    classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Environment :: Win32 (MS Windows)",
    "Environment :: MacOS X",
    "Environment :: X11 Applications",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Topic :: Artistic Software",
    "Topic :: Text Processing",
    "Topic :: Utilities"
    ],
    packages = ["scramble"],
    keywords="random text scramble"
)