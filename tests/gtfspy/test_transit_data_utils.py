import unittest

import constants
from gtfspy import TransitData, clone_transit_data, create_partial_transit_data, load_partial_transit_data
from test_utils.create_gtfs_object import create_full_transit_data


class TestTransitDataUtils(unittest.TestCase):
    def test_clone(self):
        td1 = create_full_transit_data()
        td2 = clone_transit_data(td1)
        self.assertEqual(td1, td2)

    def test_create_partial(self):
        partial = {15: ["58", "358", "458"]}
        for file_path in constants.GTFS_TEST_FILES:
            print "testing '%s'" % (file_path,)

            td1 = TransitData(gtfs_file=file_path)
            td2 = create_partial_transit_data(td1, partial)
            self.assertListEqual(sorted(agency.id for agency in td2.agencies),
                                 sorted(agency for agency in partial.iterkeys() if agency in td1.agencies))
            for agency in td2.agencies:
                if partial[agency.id] is not None:
                    self.assertListEqual(sorted(line.line_number for line in agency.lines),
                                         sorted(line.line_number for line in td1.agencies[agency.id].lines
                                                if line.line_number in partial[agency.id]))
                else:
                    self.assertListEqual(sorted(line.line_number for line in agency.lines),
                                         sorted(line.line_number for line in td1.agencies[agency.id].lines))

    def test_load_partial(self):
        lines = {15: ["58", "358", "458"]}
        for file_path in constants.GTFS_TEST_FILES:
            print "testing '%s'" % (file_path,)

            td1 = load_partial_transit_data(file_path, lines)
            td2 = create_partial_transit_data(TransitData(gtfs_file=file_path), lines)
            self.assertEqual(td1, td2)


if __name__ == '__main__':
    unittest.main()
