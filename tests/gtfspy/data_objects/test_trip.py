import unittest

from gtfspy.utils.parsing import parse_yes_no_unknown
from test_utils.create_gtfs_object import create_full_transit_data
from test_utils.test_case_utils import test_property, test_attribute

MINI_TRIP_CSV_ROW = dict(trip_id="1", route_id="1001", service_id=1)
FULL_TRIP_CSV_ROW = dict(trip_id="1", route_id="1001", service_id=1, trip_headsign="test headsign", trip_short_name="1",
                         direction_id=1, block_id=1, shape_id=1, bikes_allowed=1, wheelchair_accessible=2,
                         original_trip_id="1 origin", test_attribute="test data")
ALL_CSV_ROWS = [MINI_TRIP_CSV_ROW, FULL_TRIP_CSV_ROW]


class TestTrip(unittest.TestCase):
    def test_minimum_properties(self):
        td = create_full_transit_data()
        trip = td.trips.add(**MINI_TRIP_CSV_ROW)

        self.assertTrue(hasattr(trip, "id"))
        self.assertRaises(Exception, setattr, trip, "id", "2")

        test_property(self, trip, property_name="route", new_value=td.routes["1002"])
        test_property(self, trip, property_name="service", new_value=td.calendar[2])
        test_property(self, trip, property_name="trip_headsign", new_value="new headsign")
        test_property(self, trip, property_name="trip_short_name", new_value="2")
        test_property(self, trip, property_name="direction_id", new_value=2)
        test_property(self, trip, property_name="block_id", new_value=2)
        test_property(self, trip, property_name="shape", new_value=td.shapes[2])
        test_property(self, trip, property_name="bikes_allowed", new_value=False)
        test_property(self, trip, property_name="wheelchair_accessible", new_value=True)
        test_property(self, trip, property_name="original_trip_id", new_value="2 origin")

        self.assertNotIn("test_attribute", trip.attributes)
        test_attribute(self, trip, attribute_name="test_attribute", new_value="new test data")

    def test_maximum_properties(self):
        td = create_full_transit_data()
        trip = td.trips.add(**FULL_TRIP_CSV_ROW)

        self.assertTrue(hasattr(trip, "id"))
        self.assertRaises(Exception, setattr, trip, "id", "2")

        test_property(self, trip, property_name="route", new_value=td.routes["1002"])
        test_property(self, trip, property_name="service", new_value=td.calendar[2])
        test_property(self, trip, property_name="trip_headsign", new_value="new headsign")
        test_property(self, trip, property_name="trip_short_name", new_value="2")
        test_property(self, trip, property_name="direction_id", new_value="2")
        test_property(self, trip, property_name="block_id", new_value=2)
        test_property(self, trip, property_name="shape", new_value=td.shapes[2])
        test_property(self, trip, property_name="bikes_allowed", new_value=False)
        test_property(self, trip, property_name="wheelchair_accessible", new_value=True)
        test_property(self, trip, property_name="original_trip_id", new_value="2 origin")

        self.assertIn("test_attribute", trip.attributes)
        test_attribute(self, trip, attribute_name="test_attribute", new_value="new test data")

    def test_get_csv_line(self):
        for row in ALL_CSV_ROWS:
            td = create_full_transit_data()
            trip = td.trips.add(**row)
            self.assertDictEqual(trip.to_csv_line(), row)

    def test_get_csv_fields(self):
        for row in ALL_CSV_ROWS:
            td = create_full_transit_data()
            trip = td.trips.add(**row)
            self.assertListEqual(sorted(trip.get_csv_fields()), sorted(row.iterkeys()))

    def test_equal_operator(self):
        for row in ALL_CSV_ROWS:
            td1 = create_full_transit_data()
            td2 = create_full_transit_data()
            trip1 = td1.trips.add(**row)
            trip2 = td2.trips.add(**row)
            self.assertEqual(trip1, trip2)

    def test_not_equal_operator(self):
        original_td = create_full_transit_data()
        original_trip = original_td.trips.add(**FULL_TRIP_CSV_ROW)

        new_td = create_full_transit_data()
        row = dict(FULL_TRIP_CSV_ROW)
        row["trip_id"] = "2"
        edited_trip = new_td.trips.add(**row)
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.route = new_td.routes["1002"]
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.service = new_td.calendar[2]
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.trip_headsign = "new headsign"
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.trip_short_name = "2"
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.direction_id = 2
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.block_id = 2
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.shape = new_td.shapes[2]
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.bikes_allowed = False
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.wheelchair_accessible = True
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.original_trip_id = "2 origin"
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.attributes["test_attribute"] = "new test data"
        self.assertNotEqual(original_trip, edited_trip)

        new_td = create_full_transit_data()
        edited_trip = new_td.trips.add(**FULL_TRIP_CSV_ROW)
        edited_trip.attributes["test_attribute2"] = "new test data"
        self.assertNotEqual(original_trip, edited_trip)


class TestTripCollection(unittest.TestCase):
    def test_add(self):
        for row in ALL_CSV_ROWS:
            td = create_full_transit_data()
            starting_trips_num = len(td.trips)
            trip = td.trips.add(**row)
            self.assertIn(trip, td.trips)

            self.assertIsInstance(trip.id, str)
            self.assertEqual(trip.id, row["trip_id"])

            self.assertEqual(trip.route, td.routes[row.get("route_id")])
            self.assertEqual(trip.service, td.calendar[row.get("service_id")])
            self.assertEqual(trip.trip_headsign, row.get("trip_headsign"))
            self.assertEqual(trip.trip_short_name, row.get("trip_short_name"))
            self.assertEqual(trip.direction_id, row.get("direction_id"))
            self.assertEqual(trip.block_id, row.get("block_id"))
            self.assertEqual(trip.shape, td.shapes[row["shape_id"]] if "shape_id" in row else None)
            self.assertEqual(trip.bikes_allowed, parse_yes_no_unknown(row.get("bikes_allowed")))
            self.assertEqual(trip.wheelchair_accessible, parse_yes_no_unknown(row.get("wheelchair_accessible")))
            self.assertEqual(trip.original_trip_id, row.get("original_trip_id"))
            self.assertEqual(trip.attributes.get("test_attribute"), row.get("test_attribute"))

            self.assertEqual(len(trip.attributes), len(row) - 3)

            self.assertRaises(Exception, td.trips.add, **row)
            self.assertEqual(len(td.trips), starting_trips_num + 1)

    def test_add_object(self):
        for row in ALL_CSV_ROWS:
            source_td = create_full_transit_data()
            dest_td = create_full_transit_data()

            source_trip = source_td.trips.add(**row)
            dest_trip = dest_td.trips.add_object(source_trip)
            self.assertEqual(source_trip, dest_trip)

            trips_num = len(dest_td.trips)
            dest_td.trips.add_object(source_trip)
            self.assertEqual(trips_num, len(dest_td.trips))

            source_trip.wheelchair_accessible = not source_trip.wheelchair_accessible
            self.assertRaises(Exception, dest_td.trips.add_object, source_trip)

    def test_remove(self):
        td = create_full_transit_data()
        trip = td.trips.add(**FULL_TRIP_CSV_ROW)
        self.assertIn(trip, td.trips)
        td.trips.remove(trip)
        self.assertNotIn(trip, td.trips)
        td.trips.add(**FULL_TRIP_CSV_ROW)
        self.assertIn(trip, td.trips)
        td.trips.remove(trip.id)
        self.assertNotIn(trip, td.trips)

    def test_clean(self):
        td = create_full_transit_data()
        trip = td.trips.add(**FULL_TRIP_CSV_ROW)
        self.assertIn(trip, td.trips)
        td.trips.clean()
        self.assertNotIn(trip, td.trips)

    # TODO: test load from file
