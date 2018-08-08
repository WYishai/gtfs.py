# gtfs.py

A simple python library for parsing, editing and writing GTFS files.

GTFS (General Transit Feed Specification) is a format which determined by google in order to defines a common format for public transportation static data (schedules, stops location, etc.). For more information about the format you can read [here](https://developers.google.com/transit/gtfs) and [here](https://en.wikipedia.org/wiki/General_Transit_Feed_Specification).

## Getting Started

### Installing

You can install this package with pip.

```shell
pip install gtfs.py
```

If you want to contribute to the library code, you have to clone if from github and install it as a developer.

```shell
git clone https://github.com/WYishai/gtfs.py.git
cd gtfs.py
cd src
python setup.py develop
```

### Usage

All examples are intended for writing in a python shell (or python code file).

Creating a new TransitData object:
```python
from gtfspy import TransitData

td = TransitData()
# ...
```

Loading existing GTFS file:
```python
from gtfspy import TransitData

gtfs_file_path = "/path/to/file"
td = TransitData(gtfs_file_path)
# ...
```

Additional examples are in the [examples folder](examples) in the [GIT repository](https://github.com/WYishai/gtfs.py).

## Running the tests

This project contains unit tests that covers most of the source code. In order to run the tests, you must first install the project as a developer (as mentioned at the _Installing_ section. After the installation you can run them by typing the following commands in your shell:
```shell
cd [PROJECT_DIR]\tests
python -m unittest discover gtfspy
```
Of course, _[PROJECT_DIR]_ must be replaced by the path you cloned the GIT repository into it.

## License

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details
