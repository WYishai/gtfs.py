import unittest

from gtfspy import TransitData
from test_utils.test_case_utils import test_property

MINI_STOP_CSV_ROWS = [dict(stop_id=1, stop_name="stop name", stop_lat=31.789467, stop_lon=35.203715)]
FULL_STOP_CSV_ROWS = [dict(stop_id=1, stop_name="parent stop name", stop_lat=-31.789467, stop_lon=-35.203715,
                           location_type=1),
                      dict(stop_id=2, stop_name="stop name", stop_lat=-31.789467, stop_lon=-35.203715,
                           stop_code="10001", stop_desc="stop desc", zone_id=1, stop_url="http://stopurl.com/",
                           location_type=0, parent_station=1, stop_timezone="Asia/Jerusalem", wheelchair_boarding=True,
                           test_attribute="test data")]
ALL_CSV_ROWS = [MINI_STOP_CSV_ROWS, FULL_STOP_CSV_ROWS]


class TestStop(unittest.TestCase):
    def test_minimum_properties(self):
        td = TransitData()
        stop = None
        for row in MINI_STOP_CSV_ROWS:
            stop = td.stops.add(**row)

        self.assertTrue(hasattr(stop, "id"))
        self.assertRaises(Exception, setattr, stop, "id", 2)

        test_property(self, stop, property_name="stop_name", new_value="test name")
        test_property(self, stop, property_name="stop_lat", new_value=0)
        test_property(self, stop, property_name="stop_lon", new_value=0)
        test_property(self, stop, property_name="stop_code", new_value="1")
        test_property(self, stop, property_name="stop_desc", new_value="test desc")
        test_property(self, stop, property_name="zone_id", new_value=2)
        test_property(self, stop, property_name="stop_url", new_value="http://testurl.com/")
        test_property(self, stop, property_name="is_central_station", new_value=True)
        test_property(self, stop, property_name="parent_station", new_value=stop)
        test_property(self, stop, property_name="stop_timezone", new_value="Asia/Hebron")
        test_property(self, stop, property_name="wheelchair_boarding", new_value=True)

    def test_maximum_properties(self):
        td = TransitData()
        stop = None
        for row in FULL_STOP_CSV_ROWS:
            stop = td.stops.add(**row)

        self.assertTrue(hasattr(stop, "id"))
        self.assertRaises(Exception, setattr, stop, "id", "2")

        test_property(self, stop, property_name="stop_name", new_value="test name")
        test_property(self, stop, property_name="stop_lat", new_value=0)
        test_property(self, stop, property_name="stop_lon", new_value=0)
        test_property(self, stop, property_name="stop_code", new_value="1")
        test_property(self, stop, property_name="stop_desc", new_value="test desc")
        test_property(self, stop, property_name="zone_id", new_value=2)
        test_property(self, stop, property_name="stop_url", new_value="http://testurl.com/")
        test_property(self, stop, property_name="is_central_station", new_value=True)
        test_property(self, stop, property_name="parent_station", new_value=stop)
        test_property(self, stop, property_name="stop_timezone", new_value="Asia/Hebron")
        test_property(self, stop, property_name="wheelchair_boarding", new_value=False)

        self.assertIn("test_attribute", stop.attributes)
        stop.attributes["test_attribute"] = "new test data"
        self.assertEqual(stop.attributes["test_attribute"], "new test data")

        self.assertNotIn("test_attribute2", stop.attributes)
        stop.attributes["test_attribute2"] = "more test data"
        self.assertEqual(stop.attributes["test_attribute2"], "more test data")

    def test_get_csv_line(self):
        for rows in ALL_CSV_ROWS:
            td = TransitData()
            for row in rows:
                stop = td.stops.add(**row)
                self.assertDictEqual(stop.to_csv_line(), row)

    def test_get_csv_fields(self):
        for rows in ALL_CSV_ROWS:
            td = TransitData()
            for row in rows:
                stop = td.stops.add(**row)
                self.assertListEqual(sorted(stop.get_csv_fields()), sorted(row.iterkeys()))

    def test_equal_operator(self):
        for rows in ALL_CSV_ROWS:
            td1 = TransitData()
            td2 = TransitData()
            for row in rows:
                stop1 = td1.stops.add(**row)
                stop2 = td2.stops.add(**row)
                self.assertEqual(stop1, stop2)

    def test_not_equal_operator(self):
        original_td = TransitData()
        original_stop = None
        for row in FULL_STOP_CSV_ROWS:
            original_stop = original_td.stops.add(**row)

        new_td = TransitData()
        rows = [dict(row) for row in FULL_STOP_CSV_ROWS]
        rows[-1]["stop_id"] = 10
        edited_stop = None
        for row in rows:
            edited_stop = new_td.stops.add(**row)
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.stop_name = "test name"
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.stop_lat = 0
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.stop_lon = 0
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.stop_code = "1"
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.stop_desc = "test desc"
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.zone_id = 2
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.stop_url = "http://testurl.com/"
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.is_central_station = True
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.parent_station = None
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.stop_timezone = "Asia/Hebron"
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.wheelchair_boarding = False
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.attributes["test_attribute"] = "new test data"
        self.assertNotEqual(original_stop, edited_stop)

        new_td = TransitData()
        edited_stop = None
        for row in FULL_STOP_CSV_ROWS:
            edited_stop = new_td.stops.add(**row)
        edited_stop.attributes["test_attribute2"] = "new test data"
        self.assertNotEqual(original_stop, edited_stop)


class TestStopCollection(unittest.TestCase):
    def test_add(self):
        for rows in ALL_CSV_ROWS:
            td = TransitData()
            for row in rows:
                stop = td.stops.add(**row)
                self.assertIn(stop, td.stops)

                self.assertIsInstance(stop.id, int)
                self.assertEqual(stop.id, row["stop_id"])

                self.assertEqual(stop.stop_name, row.get("stop_name"))
                self.assertEqual(stop.stop_lat, row.get("stop_lat"))
                self.assertEqual(stop.stop_lon, row.get("stop_lon"))
                self.assertEqual(stop.is_central_station, bool(row.get("location_type", False)))
                self.assertEqual(stop.stop_code, row.get("stop_code"))
                self.assertEqual(stop.stop_desc, row.get("stop_desc"))
                self.assertEqual(stop.zone_id, row.get("zone_id"))
                self.assertEqual(stop.stop_url, row.get("stop_url"))
                self.assertEqual(stop.parent_station,
                                 td.stops[row["parent_station"]] if "parent_station" in row else None)
                self.assertEqual(stop.stop_timezone, row.get("stop_timezone"))
                self.assertEqual(stop.wheelchair_boarding, row.get("wheelchair_boarding"))
                self.assertEqual(stop.attributes.get("test_attribute"), row.get("test_attribute"))

                self.assertEqual(len(stop.attributes), len(row) - 4)

                self.assertRaises(Exception, td.stops.add, **row)

            self.assertEqual(len(td.stops), len(rows))

    def test_add_object(self):
        for rows in ALL_CSV_ROWS:
            source_td = TransitData()
            dest_td = TransitData()

            source_stop = None
            for row in rows:
                source_stop = source_td.stops.add(**row)
            dest_stop = dest_td.stops.add_object(source_stop, recursive=True)
            self.assertEqual(source_stop, dest_stop)

            stops_num = len(dest_td.stops)
            dest_td.stops.add_object(source_stop)
            self.assertEqual(stops_num, len(dest_td.stops))

            source_stop.stop_name = "test_name"
            self.assertRaises(Exception, dest_td.stops.add_object, source_stop)

    def test_remove(self):
        td = TransitData()
        stop = None
        for row in FULL_STOP_CSV_ROWS:
            stop = td.stops.add(**row)
        self.assertIn(stop, td.stops)
        td.stops.remove(stop, clean_after=False)
        self.assertNotIn(stop, td.stops)
        td.stops.add(**FULL_STOP_CSV_ROWS[-1])
        self.assertIn(stop, td.stops)
        td.stops.remove(stop.id)
        self.assertNotIn(stop, td.stops)

    def test_clean(self):
        td = TransitData()
        for row in FULL_STOP_CSV_ROWS:
            td.stops.add(**row)
        self.assertGreater(len(td.stops), 0)
        td.stops.clean()
        self.assertEqual(len(td.stops), 0)

    # TODO: test load from file
