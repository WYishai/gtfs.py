from setuptools import setup, find_packages

setup(
    name="gtfs.py",
    version="0.1",
    packages=find_packages(),

    author="Yishai Wiesner",
    author_email="wyishai AT gmail DOT com",
    description="A simple python library for parsing, editing and writing GTFS files",
    install_requires=['sortedcontainers'],
    url="https://github.com/WYishai/gtfs.py",
    classifiers=[
        "Programming Language :: Python :: 2.7"
    ],
)
