import argparse
import os

from gtfspy import TransitData

DEFAULT_GTFS_FILE_PATH = os.path.join("..", "tests", "resources", "test_gtfs.zip")


def load_gtfs(gtfs_file_path):
    td = TransitData(gtfs_file_path)
    print "TransitData object contains:"
    print "%d agencies" % (len(td.agencies))
    print "%d routes" % (len(td.routes))
    print "%d trips" % (len(td.trips))
    print "%d stops" % (len(td.stops))
    print "%d shapes" % (len(td.shapes))
    print "%d services" % (len(td.calendar))

    return td


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--gtfs-file-path", default=DEFAULT_GTFS_FILE_PATH)

    args = parser.parse_args()
    gtfs_file_path = args.gtfs_file_path

    load_gtfs(gtfs_file_path)


if __name__ == '__main__':
    main()
