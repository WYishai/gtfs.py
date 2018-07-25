import os
import tempfile
import unittest

import constants
from gtfspy import TransitData
from test_utils.gtfs_utils import compare_gtfs_files


class TestTransitDataLoad(unittest.TestCase):
    def test_load_from_file_path(self):
        for file_path in constants.GTFS_TEST_FILES:
            print "testing '%s'" % (file_path,)

            td1 = TransitData(gtfs_file=file_path)
            with open(file_path, "rb") as f:
                td2 = TransitData(gtfs_file=f)

            self.assertEqual(td1, td2)

    def test_import_export(self):
        for file_path in constants.GTFS_TEST_FILES:
            print "testing '%s'" % (file_path,)

            temp_file_path = tempfile.mktemp() + ".zip"
            try:
                td1 = TransitData(gtfs_file=file_path)
                td1.save(temp_file_path)
                td2 = TransitData(temp_file_path)
                self.assertEqual(td1, td2)

                compare_gtfs_files(file_path, temp_file_path, self)
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

    def test_clean(self):
        td = create_full_transit_data()
        for trip in td.trips:
            for stop_time in list(trip.stop_times):
                stop_time.trip.stop_times.remove(stop_time)
                stop_time.stop.stop_times.remove(stop_time)

        td.clean()

        self.assertEqual(0, len(td.agencies))
        self.assertEqual(0, len(td.routes))
        self.assertEqual(0, len(td.trips))
        self.assertEqual(0, len(td.shapes))
        self.assertEqual(0, len(td.calendar))
        self.assertEqual(0, len(td.stops))
        self.assertEqual(0, len(td.fare_attributes))
        self.assertEqual(0, len(td.fare_rules))


if __name__ == '__main__':
    unittest.main()
