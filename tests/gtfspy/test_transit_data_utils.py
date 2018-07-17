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
        lines = {15: ["58", "358", "458"]}
        td1 = TransitData(gtfs_file=constants.GTFS_TEST_FILE_PATH)
        td2 = create_partial_transit_data(td1, lines)
        self.assertEqual(sorted(agency.id for agency in td2.agencies), sorted(lines.iterkeys()))
        for agency in td2.agencies:
            self.assertEqual(sorted(lines[agency.id]), sorted(line.line_number for line in agency.lines))

    def test_load_partial(self):
        lines = {15: ["58", "358", "458"]}
        td1 = load_partial_transit_data(constants.GTFS_TEST_FILE_PATH, lines)
        td2 = create_partial_transit_data(TransitData(gtfs_file=constants.GTFS_TEST_FILE_PATH), lines)
        self.assertEqual(td1, td2)


if __name__ == '__main__':
    unittest.main()
