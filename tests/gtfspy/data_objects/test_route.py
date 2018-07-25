import unittest

from test_utils.create_gtfs_object import create_full_transit_data
from test_utils.test_case_utils import test_property, test_attribute

MINI_ROUTE_CSV_ROW = dict(route_id="1", route_short_name="1", route_long_name="test route", route_type=3, agency_id=1)
FULL_ROUTE_CSV_ROW = dict(route_id="1", route_short_name="1", route_long_name="test route", route_type=3, agency_id=1,
                          route_desc="route desc", route_url="http://routeurl.com/", route_color="FF9933",
                          route_text_color="0077CC", route_sort_order=1, test_attribute="test data")
ALL_CSV_ROWS = [MINI_ROUTE_CSV_ROW, FULL_ROUTE_CSV_ROW]


class TestRoute(unittest.TestCase):
    def test_minimum_properties(self):
        td = create_full_transit_data()
        route = td.routes.add(**MINI_ROUTE_CSV_ROW)

        self.assertTrue(hasattr(route, "id"))
        self.assertRaises(Exception, setattr, route, "id", "2")

        test_property(self, route, property_name="route_short_name", new_value="2")
        test_property(self, route, property_name="route_long_name", new_value="new name")
        test_property(self, route, property_name="route_type", new_value=2)
        test_property(self, route, property_name="agency", new_value=td.agencies[15])
        test_property(self, route, property_name="route_desc", new_value="new route desc")
        test_property(self, route, property_name="route_url", new_value="http://testurl.com/")
        test_property(self, route, property_name="route_color", new_value="FFFF00")
        test_property(self, route, property_name="route_text_color", new_value="0000FF")
        test_property(self, route, property_name="route_sort_order", new_value=2)

        self.assertNotIn("test_attribute", route.attributes)
        test_attribute(self, route, attribute_name="test_attribute", new_value="new test data")

    def test_maximum_properties(self):
        td = create_full_transit_data()
        route = td.routes.add(**FULL_ROUTE_CSV_ROW)

        self.assertTrue(hasattr(route, "id"))
        self.assertRaises(Exception, setattr, route, "id", "2")

        test_property(self, route, property_name="route_short_name", new_value="2")
        test_property(self, route, property_name="route_long_name", new_value="new name")
        test_property(self, route, property_name="route_type", new_value=2)
        test_property(self, route, property_name="agency", new_value=td.agencies[15])
        test_property(self, route, property_name="route_desc", new_value="new route desc")
        test_property(self, route, property_name="route_url", new_value="http://testurl.com/")
        test_property(self, route, property_name="route_color", new_value="FFFF00")
        test_property(self, route, property_name="route_text_color", new_value="0000FF")
        test_property(self, route, property_name="route_sort_order", new_value=2)

        self.assertIn("test_attribute", route.attributes)
        test_attribute(self, route, attribute_name="test_attribute", new_value="new test data")

    def test_get_csv_line(self):
        for row in ALL_CSV_ROWS:
            td = create_full_transit_data()
            route = td.routes.add(**row)
            self.assertDictEqual(route.to_csv_line(), row)

    def test_get_csv_fields(self):
        for row in ALL_CSV_ROWS:
            td = create_full_transit_data()
            route = td.routes.add(**row)
            self.assertListEqual(sorted(route.get_csv_fields()), sorted(row.iterkeys()))

    def test_equal_operator(self):
        for row in ALL_CSV_ROWS:
            td1 = create_full_transit_data()
            td2 = create_full_transit_data()
            route1 = td1.routes.add(**row)
            route2 = td2.routes.add(**row)
            self.assertEqual(route1, route2)

    def test_not_equal_operator(self):
        original_td = create_full_transit_data()
        original_route = original_td.routes.add(**FULL_ROUTE_CSV_ROW)

        new_td = create_full_transit_data()
        row = dict(FULL_ROUTE_CSV_ROW)
        row["route_id"] = "10"
        edited_route = new_td.routes.add(**row)
        self.assertNotEqual(original_route, edited_route)

        new_td = create_full_transit_data()
        edited_route = new_td.routes.add(**FULL_ROUTE_CSV_ROW)
        edited_route.route_short_name = "2"
        self.assertNotEqual(original_route, edited_route)

        new_td = create_full_transit_data()
        edited_route = new_td.routes.add(**FULL_ROUTE_CSV_ROW)
        edited_route.route_long_name = "new name"
        self.assertNotEqual(original_route, edited_route)

        new_td = create_full_transit_data()
        edited_route = new_td.routes.add(**FULL_ROUTE_CSV_ROW)
        edited_route.agency = new_td.agencies[15]
        self.assertNotEqual(original_route, edited_route)

        new_td = create_full_transit_data()
        edited_route = new_td.routes.add(**FULL_ROUTE_CSV_ROW)
        edited_route.route_desc = "new route desc"
        self.assertNotEqual(original_route, edited_route)

        new_td = create_full_transit_data()
        edited_route = new_td.routes.add(**FULL_ROUTE_CSV_ROW)
        edited_route.route_url = "http://testurl.com/"
        self.assertNotEqual(original_route, edited_route)

        new_td = create_full_transit_data()
        edited_route = new_td.routes.add(**FULL_ROUTE_CSV_ROW)
        edited_route.route_color = "FFFF00"
        self.assertNotEqual(original_route, edited_route)

        new_td = create_full_transit_data()
        edited_route = new_td.routes.add(**FULL_ROUTE_CSV_ROW)
        edited_route.route_text_color = "0000FF"
        self.assertNotEqual(original_route, edited_route)

        new_td = create_full_transit_data()
        edited_route = new_td.routes.add(**FULL_ROUTE_CSV_ROW)
        edited_route.route_sort_order = 2
        self.assertNotEqual(original_route, edited_route)

        new_td = create_full_transit_data()
        edited_route = new_td.routes.add(**FULL_ROUTE_CSV_ROW)
        edited_route.attributes["test_attribute"] = "new test data"
        self.assertNotEqual(original_route, edited_route)

        new_td = create_full_transit_data()
        edited_route = new_td.routes.add(**FULL_ROUTE_CSV_ROW)
        edited_route.attributes["test_attribute2"] = "new test data"
        self.assertNotEqual(original_route, edited_route)


class TestRouteCollection(unittest.TestCase):
    def test_add(self):
        for row in ALL_CSV_ROWS:
            td = create_full_transit_data()
            starting_routes_num = len(td.routes)
            route = td.routes.add(**row)
            self.assertIn(route, td.routes)

            self.assertIsInstance(route.id, str)
            self.assertEqual(route.id, row["route_id"])

            self.assertEqual(route.route_short_name, row.get("route_short_name"))
            self.assertEqual(route.route_long_name, row.get("route_long_name"))
            self.assertEqual(route.route_type, row.get("route_type"))
            self.assertEqual(route.agency, td.agencies[row.get("agency_id")])
            self.assertEqual(route.route_desc, row.get("route_desc"))
            self.assertEqual(route.route_url, row.get("route_url"))
            self.assertEqual(route.route_color, row.get("route_color"))
            self.assertEqual(route.route_text_color, row.get("route_text_color"))
            self.assertEqual(route.route_sort_order, row.get("route_sort_order"))
            self.assertEqual(route.attributes.get("test_attribute"), row.get("test_attribute"))

            self.assertEqual(len(route.attributes), len(row) - 5)

            self.assertRaises(Exception, td.routes.add, **row)
            self.assertEqual(len(td.routes), starting_routes_num + 1)

    def test_add_object(self):
        for row in ALL_CSV_ROWS:
            source_td = create_full_transit_data()
            dest_td = create_full_transit_data()

            source_route = source_td.routes.add(**row)
            dest_route = dest_td.routes.add_object(source_route)
            self.assertEqual(source_route, dest_route)

            routes_num = len(dest_td.routes)
            dest_td.routes.add_object(source_route)
            self.assertEqual(routes_num, len(dest_td.routes))

            source_route.route_short_name = "2"
            self.assertRaises(Exception, dest_td.routes.add_object, source_route)

    def test_remove(self):
        td = create_full_transit_data()
        route = td.routes.add(**FULL_ROUTE_CSV_ROW)
        self.assertIn(route, td.routes)
        td.routes.remove(route)
        self.assertNotIn(route, td.routes)
        td.routes.add(**FULL_ROUTE_CSV_ROW)
        self.assertIn(route, td.routes)
        td.routes.remove(route.id)
        self.assertNotIn(route, td.routes)

    def test_clean(self):
        td = create_full_transit_data()
        route = td.routes.add(**FULL_ROUTE_CSV_ROW)
        self.assertIn(route, td.routes)
        td.routes.clean()
        self.assertNotIn(route, td.routes)

    # TODO: test load from file
