import unittest

from gtfspy import TransitData
from test_utils.test_case_utils import test_property

MINI_FARE_ATTRIBUTE_CSV_ROW = dict(fare_id="1", price="5.60", currency_type="ILS", payment_method=0, transfers=0)
FULL_FARE_ATTRIBUTE_CSV_ROW = dict(fare_id="1", price="5.60", currency_type="ILS", payment_method=0, transfers=0,
                                   transfer_duration=1, test_attribute="test data")
ALL_CSV_ROWS = [MINI_FARE_ATTRIBUTE_CSV_ROW, FULL_FARE_ATTRIBUTE_CSV_ROW]


class TestFareAttribute(unittest.TestCase):
    def test_minimum_properties(self):
        td = TransitData()
        fare_attribute = td.fare_attributes.add(**MINI_FARE_ATTRIBUTE_CSV_ROW)

        self.assertTrue(hasattr(fare_attribute, "id"))
        self.assertRaises(Exception, setattr, fare_attribute, "id", "2")

        test_property(self, fare_attribute, property_name="price", new_value=1)
        test_property(self, fare_attribute, property_name="currency_type", new_value="USD")
        test_property(self, fare_attribute, property_name="payment_method", new_value=1)
        test_property(self, fare_attribute, property_name="transfers", new_value=1)
        test_property(self, fare_attribute, property_name="transfer_duration", new_value=2)

    def test_maximum_properties(self):
        td = TransitData()
        fare_attribute = td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)

        self.assertTrue(hasattr(fare_attribute, "id"))
        self.assertRaises(Exception, setattr, fare_attribute, "id", "2")

        test_property(self, fare_attribute, property_name="price", new_value=1)
        test_property(self, fare_attribute, property_name="currency_type", new_value="USD")
        test_property(self, fare_attribute, property_name="payment_method", new_value=1)
        test_property(self, fare_attribute, property_name="transfers", new_value=1)
        test_property(self, fare_attribute, property_name="transfer_duration", new_value=2)

        self.assertIn("test_attribute", fare_attribute.attributes)
        fare_attribute.attributes["test_attribute"] = "new test data"
        self.assertEqual(fare_attribute.attributes["test_attribute"], "new test data")

        self.assertNotIn("test_attribute2", fare_attribute.attributes)
        fare_attribute.attributes["test_attribute2"] = "more test data"
        self.assertEqual(fare_attribute.attributes["test_attribute2"], "more test data")

    def test_get_csv_line(self):
        for row in ALL_CSV_ROWS:
            td = TransitData()
            fare_attribute = td.fare_attributes.add(**row)
            self.assertDictEqual(fare_attribute.to_csv_line(), row)

    def test_get_csv_fields(self):
        for row in ALL_CSV_ROWS:
            td = TransitData()
            fare_attribute = td.fare_attributes.add(**row)
            self.assertListEqual(sorted(fare_attribute.get_csv_fields()), sorted(row.iterkeys()))

    def test_equal_operator(self):
        for row in ALL_CSV_ROWS:
            td1 = TransitData()
            td2 = TransitData()
            fare_attribute1 = td1.fare_attributes.add(**row)
            fare_attribute2 = td2.fare_attributes.add(**row)
            self.assertEqual(fare_attribute1, fare_attribute2)

    def test_not_equal_operator(self):
        original_td = TransitData()
        original_fare_attribute = original_td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)

        new_td = TransitData()
        row = dict(FULL_FARE_ATTRIBUTE_CSV_ROW)
        row["fare_id"] = "10"
        edited_fare_attribute = new_td.fare_attributes.add(**row)
        self.assertNotEqual(original_fare_attribute, edited_fare_attribute)

        new_td = TransitData()
        edited_fare_attribute = new_td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)
        edited_fare_attribute.price = 1
        self.assertNotEqual(original_fare_attribute, edited_fare_attribute)

        new_td = TransitData()
        edited_fare_attribute = new_td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)
        edited_fare_attribute.currency_type = "USD"
        self.assertNotEqual(original_fare_attribute, edited_fare_attribute)

        new_td = TransitData()
        edited_fare_attribute = new_td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)
        edited_fare_attribute.payment_method = 1
        self.assertNotEqual(original_fare_attribute, edited_fare_attribute)

        new_td = TransitData()
        edited_fare_attribute = new_td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)
        edited_fare_attribute.transfers = 1
        self.assertNotEqual(original_fare_attribute, edited_fare_attribute)

        new_td = TransitData()
        edited_fare_attribute = new_td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)
        edited_fare_attribute.transfer_duration = 2
        self.assertNotEqual(original_fare_attribute, edited_fare_attribute)

        new_td = TransitData()
        edited_fare_attribute = new_td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)
        edited_fare_attribute.attributes["test_attribute"] = "new test data"
        self.assertNotEqual(original_fare_attribute, edited_fare_attribute)

        new_td = TransitData()
        edited_fare_attribute = new_td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)
        edited_fare_attribute.attributes["test_attribute2"] = "new test data"
        self.assertNotEqual(original_fare_attribute, edited_fare_attribute)


class TestFareAttributeCollection(unittest.TestCase):
    def test_add(self):
        for row in ALL_CSV_ROWS:
            td = TransitData()
            fare_attribute = td.fare_attributes.add(**row)
            self.assertIn(fare_attribute, td.fare_attributes)

            self.assertIsInstance(fare_attribute.id, str)
            self.assertEqual(fare_attribute.id, row["fare_id"])

            self.assertEqual(fare_attribute.price, float(row.get("price")))
            self.assertEqual(fare_attribute.currency_type, row.get("currency_type"))
            self.assertEqual(fare_attribute.payment_method, row.get("payment_method"))
            self.assertEqual(fare_attribute.transfers, row.get("transfers"))
            self.assertEqual(fare_attribute.transfer_duration, row.get("transfer_duration"))
            self.assertEqual(fare_attribute.attributes.get("test_attribute"), row.get("test_attribute"))

            self.assertEqual(len(fare_attribute.attributes), len(row) - 5)

            self.assertRaises(Exception, td.fare_attributes.add, **row)
            self.assertEqual(len(td.fare_attributes), 1)

    def test_add_object(self):
        for row in ALL_CSV_ROWS:
            source_td = TransitData()
            dest_td = TransitData()

            source_fare_attribute = source_td.fare_attributes.add(**row)
            dest_fare_attribute = dest_td.fare_attributes.add_object(source_fare_attribute)
            self.assertEqual(source_fare_attribute, dest_fare_attribute)

            fare_attributes_num = len(dest_td.fare_attributes)
            dest_td.fare_attributes.add_object(source_fare_attribute)
            self.assertEqual(fare_attributes_num, len(dest_td.fare_attributes))

            source_fare_attribute.price = 2.4
            self.assertRaises(Exception, dest_td.fare_attributes.add_object, source_fare_attribute)

    def test_remove(self):
        td = TransitData()
        fare_attribute = td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)
        self.assertIn(fare_attribute, td.fare_attributes)
        td.fare_attributes.remove(fare_attribute)
        self.assertNotIn(fare_attribute, td.fare_attributes)
        td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)
        self.assertIn(fare_attribute, td.fare_attributes)
        td.fare_attributes.remove(fare_attribute.id)
        self.assertNotIn(fare_attribute, td.fare_attributes)

    def test_clean(self):
        td = TransitData()
        td.fare_attributes.add(**FULL_FARE_ATTRIBUTE_CSV_ROW)
        self.assertGreater(len(td.fare_attributes), 0)
        td.fare_attributes.clean()
        self.assertEqual(len(td.fare_attributes), 0)

    # TODO: test load from file
