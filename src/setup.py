import os

from setuptools import setup, find_packages

with open(os.path.join("..", "README.md"), "r") as readme_file:
    long_description = readme_file.read()
    long_description = long_description \
        .replace("](examples)", "](https://github.com/WYishai/gtfs.py/blob/master/examples)") \
        .replace("](LICENSE)", "](https://github.com/WYishai/gtfs.py/blob/master/LICENSE)")

setup(
    name="gtfs.py",
    version="0.1",
    packages=find_packages(),

    author="Yishai Wiesner",
    author_email="wyishai@gmail.com",
    description="A simple python library for parsing, editing and writing GTFS files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["sortedcontainers"],
    url="https://github.com/WYishai/gtfs.py",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
