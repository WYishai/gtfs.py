import unittest
from datetime import timedelta

from test_utils.create_gtfs_object import create_full_transit_data
from test_utils.test_case_utils import test_property, test_attribute

MINI_STOP_TIME_CSV_ROW = dict(trip_id="1001_1", arrival_time="01:00:00", departure_time="01:00:00", stop_id=10001,
                              stop_sequence=3)
FULL_STOP_TIME_CSV_ROW = dict(trip_id="1001_1", arrival_time="01:00:00", departure_time="02:00:00", stop_id=10001,
                              stop_sequence=3, pickup_type=1, drop_off_type=0, shape_dist_traveled=0,
                              stop_headsign="stop headsign", timepoint=0, test_attribute="test data")
ALL_CSV_ROWS = [MINI_STOP_TIME_CSV_ROW, FULL_STOP_TIME_CSV_ROW]


class TestStopTime(unittest.TestCase):
    def test_minimum_properties(self):
        td = create_full_transit_data()
        stop_time = td.add_stop_time(**MINI_STOP_TIME_CSV_ROW)

        test_property(self, stop_time, property_name="trip", new_value=td.trips["1001_2"])
        test_property(self, stop_time, property_name="arrival_time", new_value=timedelta(hours=2))
        test_property(self, stop_time, property_name="departure_time", new_value=timedelta(hours=3))
        test_property(self, stop_time, property_name="stop", new_value=td.stops[20000])
        test_property(self, stop_time, property_name="stop_sequence", new_value=1)
        test_property(self, stop_time, property_name="pickup_type", new_value=2)
        test_property(self, stop_time, property_name="drop_off_type", new_value=2)
        test_property(self, stop_time, property_name="allow_pickup", new_value=not stop_time.allow_pickup)
        test_property(self, stop_time, property_name="allow_drop_off", new_value=not stop_time.allow_drop_off)
        test_property(self, stop_time, property_name="shape_dist_traveled", new_value=1)
        test_property(self, stop_time, property_name="stop_headsign", new_value="new headsign")
        test_property(self, stop_time, property_name="is_exact_time", new_value=not stop_time.is_exact_time)

        self.assertNotIn("test_attribute", stop_time.attributes)
        test_attribute(self, stop_time, attribute_name="test_attribute", new_value="new test data")

    def test_maximum_properties(self):
        td = create_full_transit_data()
        stop_time = td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)

        test_property(self, stop_time, property_name="trip", new_value=td.trips["1001_2"])
        test_property(self, stop_time, property_name="arrival_time", new_value=timedelta(hours=2))
        test_property(self, stop_time, property_name="departure_time", new_value=timedelta(hours=3))
        test_property(self, stop_time, property_name="stop", new_value=td.stops[20000])
        test_property(self, stop_time, property_name="stop_sequence", new_value=1)
        test_property(self, stop_time, property_name="pickup_type", new_value=2)
        test_property(self, stop_time, property_name="drop_off_type", new_value=2)
        test_property(self, stop_time, property_name="allow_pickup", new_value=False)
        test_property(self, stop_time, property_name="allow_drop_off", new_value=False)
        test_property(self, stop_time, property_name="shape_dist_traveled", new_value=1)
        test_property(self, stop_time, property_name="stop_headsign", new_value="new headsign")
        test_property(self, stop_time, property_name="is_exact_time", new_value=not stop_time.is_exact_time)

        self.assertIn("test_attribute", stop_time.attributes)
        test_attribute(self, stop_time, attribute_name="test_attribute", new_value="new test data")

    def test_get_csv_line(self):
        for row in ALL_CSV_ROWS:
            td = create_full_transit_data()
            stop_time = td.add_stop_time(**row)
            self.assertDictEqual(stop_time.to_csv_line(), row)

    def test_get_csv_fields(self):
        for row in ALL_CSV_ROWS:
            td = create_full_transit_data()
            stop_time = td.add_stop_time(**row)
            self.assertListEqual(sorted(stop_time.get_csv_fields()), sorted(row.iterkeys()))

    def test_equal_operator(self):
        for row in ALL_CSV_ROWS:
            td1 = create_full_transit_data()
            td2 = create_full_transit_data()
            stop_time1 = td1.add_stop_time(**row)
            stop_time2 = td2.add_stop_time(**row)
            self.assertEqual(stop_time1, stop_time2)

    def test_not_equal_operator(self):
        original_td = create_full_transit_data()
        original_stop_time = original_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.trip = new_td.trips["1001_2"]
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.arrival_time = timedelta(hours=2)
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.departure_time = timedelta(hours=3)
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.stop = new_td.stops[20000]
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.stop_sequence = 1
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.pickup_type = 2
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.drop_off_type = 2
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.allow_pickup = not edited_stop_time.allow_pickup
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.allow_drop_off = not edited_stop_time.allow_drop_off
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.shape_dist_traveled = 1
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.stop_headsign = "new headsign"
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.is_exact_time = not edited_stop_time.is_exact_time
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.attributes["test_attribute"] = "new test data"
        self.assertNotEqual(original_stop_time, edited_stop_time)

        new_td = create_full_transit_data()
        edited_stop_time = new_td.add_stop_time(**FULL_STOP_TIME_CSV_ROW)
        edited_stop_time.attributes["test_attribute2"] = "new test data"
        self.assertNotEqual(original_stop_time, edited_stop_time)
