import unittest

from gtfspy import TransitData, clone_transit_data, create_partial_transit_data, load_partial_transit_data

import constants


class TestTransitDataUtils(unittest.TestCase):
    def test_clone(self):
        td1 = TransitData(gtfs_file=constants.GTFS_TEST_FILE_PATH)
        td2 = clone_transit_data(td1)
        self.assertEqual(td1, td2)

    def test_create_partial(self):
        lines = {15: ["58", "358", "458"]}
        td1 = TransitData(gtfs_file=constants.GTFS_TEST_FILE_PATH)
        td2 = create_partial_transit_data(td1, lines)
        self.assertEqual(len(td2.agencies), len(lines.keys()))
        self.assertEqual(sorted(agency.agency_id for agency in td2.agencies), sorted(lines.iterkeys()))

    def test_load_partial(self):
        lines = {15: ["58", "358", "458"]}
        td1 = load_partial_transit_data(constants.GTFS_TEST_FILE_PATH, lines)
        td2 = create_partial_transit_data(TransitData(gtfs_file=constants.GTFS_TEST_FILE_PATH), lines)
        self.assertEqual(td1, td2)


if __name__ == '__main__':
    unittest.main()
