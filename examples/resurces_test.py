import argparse
import gc
import logging
import os
import time
from datetime import datetime

import psutil

from gtfspy.transit_data_object import TransitData

DEFAULT_GTFS_FILE_PATH = os.path.join("..", "tests", "resources", "test_gtfs.zip")


def pretty_size(bytes_num):
    sizes = ["Bi", "KiB", "MiB", "GiB", "TiB", "PiB"]
    bytes_num = float(bytes_num)
    i = 0
    while bytes_num >= 1024:
        bytes_num /= 1024
        i += 1

    return "%s %s" % (round(bytes_num, 2), sizes[i])


def check_resources(gtfs_file_path):
    process = psutil.Process(os.getpid())

    start_memory = process.memory_info().vms
    logging.info("Start our's")
    start = datetime.now()
    td = TransitData(gtfs_file_path)
    logging.info("End our's. duration: %s" % (datetime.now() - start,))
    logging.info("Memory usage: %s (%s)" % (pretty_size(process.memory_info().vms - start_memory),
                                            pretty_size(process.memory_info().vms)))

    del td
    gc.collect()
    time.sleep(30)
    uo = gc.collect()
    logging.info("Unreachable objects: %s" % (uo,))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--gtfs-file-path", default=DEFAULT_GTFS_FILE_PATH)

    args = parser.parse_args()
    gtfs_file_path = args.gtfs_file_path

    check_resources(gtfs_file_path)


if __name__ == '__main__':
    main()
