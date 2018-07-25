import argparse
import os
from datetime import datetime

from gtfspy import TransitData, create_partial_transit_data, load_partial_transit_data

DEFAULT_GTFS_FILE_PATH = os.path.join("..", "tests", "resources", "minimized_real_gtfs.zip")


def load_partial_gtfs1(file_path, partial):
    """
    :type file_path: str
    :type partial: dict[int, list[str]] | dict[int, None]
    """

    td = load_partial_transit_data(file_path, partial)

    print "TransitData object contains:"
    print "%d agencies" % (len(td.agencies))
    print "%d routes" % (len(td.routes))
    print "%d trips" % (len(td.trips))
    print "%d stops" % (len(td.stops))
    print "%d shapes" % (len(td.shapes))
    print "%d services" % (len(td.calendar))

    return td


def load_partial_gtfs2(file_path, partial):
    """
    :type file_path: str
    :type partial: dict[int, list[str]] | dict[int, None]
    """

    td = TransitData(file_path)
    td = create_partial_transit_data(td, partial)

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
    parser.add_argument("-f", "--gtfs-file-path", default=DEFAULT_GTFS_FILE_PATH)
    parser.add_argument("-p", "--partial", type=int, default=15)

    args = parser.parse_args()
    gtfs_file_path = args.gtfs_file_path
    partial = {args.partial: None}

    start = datetime.now()
    td = load_partial_gtfs1(gtfs_file_path, partial)
    print "Took %s\n" % (datetime.now() - start,)

    start = datetime.now()
    td = load_partial_gtfs2(gtfs_file_path, partial)
    print "Took %s\n" % (datetime.now() - start,)


if __name__ == '__main__':
    main()
