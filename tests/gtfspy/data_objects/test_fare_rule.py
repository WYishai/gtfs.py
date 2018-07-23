import unittest

from test_utils.create_gtfs_object import create_full_transit_data
from test_utils.test_case_utils import test_property, test_attribute

MINI_FARE_RULE_CSV_ROW = dict(fare_id="1")
FULL_FARE_RULE_CSV_ROW = dict(fare_id="1", route_id="1001", origin_id=7, destination_id=8, contains_id=8,
                              test_attribute="test data")
ALL_CSV_ROWS = [MINI_FARE_RULE_CSV_ROW, FULL_FARE_RULE_CSV_ROW]


class TestFareRule(unittest.TestCase):
    def test_minimum_properties(self):
        td = create_full_transit_data()
        fare_rule = td.fare_rules.add(**MINI_FARE_RULE_CSV_ROW)

        test_property(self, fare_rule, property_name="fare", new_value=td.fare_attributes["2"])
        test_property(self, fare_rule, property_name="route", new_value=td.routes["1002"])
        test_property(self, fare_rule, property_name="origin_id", new_value=1)
        test_property(self, fare_rule, property_name="destination_id", new_value=1)
        test_property(self, fare_rule, property_name="contains_id", new_value=1)

        self.assertNotIn("test_attribute", fare_rule.attributes)
        test_attribute(self, fare_rule, attribute_name="test_attribute", new_value="new test data")

    def test_maximum_properties(self):
        td = create_full_transit_data()
        fare_rule = td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)

        test_property(self, fare_rule, property_name="fare", new_value=td.fare_attributes["2"])
        test_property(self, fare_rule, property_name="route", new_value=td.routes["1002"])
        test_property(self, fare_rule, property_name="origin_id", new_value=2)
        test_property(self, fare_rule, property_name="destination_id", new_value=1)
        test_property(self, fare_rule, property_name="contains_id", new_value=1)

        self.assertIn("test_attribute", fare_rule.attributes)
        test_attribute(self, fare_rule, attribute_name="test_attribute", new_value="new test data")

    def test_get_csv_line(self):
        for row in ALL_CSV_ROWS:
            td = create_full_transit_data()
            fare_rule = td.fare_rules.add(**row)
            self.assertDictEqual(fare_rule.to_csv_line(), row)

    def test_get_csv_fields(self):
        for row in ALL_CSV_ROWS:
            td = create_full_transit_data()
            fare_rule = td.fare_rules.add(**row)
            self.assertListEqual(sorted(fare_rule.get_csv_fields()), sorted(row.iterkeys()))

    def test_equal_operator(self):
        for row in ALL_CSV_ROWS:
            td1 = create_full_transit_data()
            td2 = create_full_transit_data()
            fare_rule1 = td1.fare_rules.add(**row)
            fare_rule2 = td2.fare_rules.add(**row)
            self.assertEqual(fare_rule1, fare_rule2)

    def test_not_equal_operator(self):
        original_td = create_full_transit_data()
        original_fare_rule = original_td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)

        new_td = create_full_transit_data()
        edited_fare_rule = new_td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)
        edited_fare_rule.fare = new_td.fare_attributes["2"]
        self.assertNotEqual(original_fare_rule, edited_fare_rule)

        new_td = create_full_transit_data()
        edited_fare_rule = new_td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)
        edited_fare_rule.route = new_td.routes["1002"]
        self.assertNotEqual(original_fare_rule, edited_fare_rule)

        new_td = create_full_transit_data()
        edited_fare_rule = new_td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)
        edited_fare_rule.origin_id = 2
        self.assertNotEqual(original_fare_rule, edited_fare_rule)

        new_td = create_full_transit_data()
        edited_fare_rule = new_td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)
        edited_fare_rule.destination_id = 1
        self.assertNotEqual(original_fare_rule, edited_fare_rule)

        new_td = create_full_transit_data()
        edited_fare_rule = new_td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)
        edited_fare_rule.contains_id = 1
        self.assertNotEqual(original_fare_rule, edited_fare_rule)

        new_td = create_full_transit_data()
        edited_fare_rule = new_td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)
        edited_fare_rule.attributes["test_attribute"] = "new test data"
        self.assertNotEqual(original_fare_rule, edited_fare_rule)

        new_td = create_full_transit_data()
        edited_fare_rule = new_td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)
        edited_fare_rule.attributes["test_attribute2"] = "new test data"
        self.assertNotEqual(original_fare_rule, edited_fare_rule)


class TestFareRuleCollection(unittest.TestCase):
    def test_add(self):
        for row in ALL_CSV_ROWS:
            td = create_full_transit_data()
            starting_fare_rules_num = len(td.fare_rules)
            fare_rule = td.fare_rules.add(**row)
            self.assertIn(fare_rule, td.fare_rules)

            self.assertEqual(fare_rule.fare, td.fare_attributes[row.get("fare_id")])
            self.assertEqual(fare_rule.route, td.routes[row.get("route_id")] if "route_id" in row else None)
            self.assertEqual(fare_rule.origin_id, row.get("origin_id"))
            self.assertEqual(fare_rule.destination_id, row.get("destination_id"))
            self.assertEqual(fare_rule.contains_id, row.get("contains_id"))

            self.assertEqual(len(fare_rule.attributes), len(row) - 1)

            # self.assertRaises(Exception, td.fare_rules.add, **row)
            self.assertEqual(len(td.fare_rules), starting_fare_rules_num + 1)

    def test_add_object(self):
        for row in ALL_CSV_ROWS:
            source_td = create_full_transit_data()
            dest_td = create_full_transit_data()

            source_fare_rule = source_td.fare_rules.add(**row)
            dest_fare_rule = dest_td.fare_rules.add_object(source_fare_rule)
            self.assertEqual(source_fare_rule, dest_fare_rule)

            # fare_rules_num = len(dest_td.fare_rules)
            # dest_td.fare_rules.add_object(source_fare_rule)
            # self.assertEqual(fare_rules_num, len(dest_td.fare_rules))
            #
            # source_fare_rule.wheelchair_accessible = not source_fare_rule.wheelchair_accessible
            # self.assertRaises(Exception, dest_td.fare_rules.add_object, source_fare_rule)

    def test_remove(self):
        td = create_full_transit_data()
        fare_rule = td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)
        self.assertIn(fare_rule, td.fare_rules)
        td.fare_rules.remove(fare_rule)
        self.assertNotIn(fare_rule, td.fare_rules)
        td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)
        self.assertIn(fare_rule, td.fare_rules)
        td.fare_rules.remove(fare_rule)
        self.assertNotIn(fare_rule, td.fare_rules)

    def test_clean(self):
        td = create_full_transit_data()
        trip = td.fare_rules.add(**FULL_FARE_RULE_CSV_ROW)
        self.assertIn(trip, td.fare_rules)
        td.fare_rules.clean()
        self.assertNotIn(trip, td.fare_rules)

    # TODO: test load from file
