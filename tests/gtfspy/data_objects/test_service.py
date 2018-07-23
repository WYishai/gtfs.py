import unittest
from datetime import date, timedelta

from gtfspy import TransitData
from test_utils.test_case_utils import test_property

TODAY_DATE = date.today()
TOMORROW_DATE = date.today() + timedelta(days=1)
TODAY_DATE_STR = TODAY_DATE.strftime("%Y%m%d")
TOMORROW_DATE_STR = TOMORROW_DATE.strftime("%Y%m%d")

MINI_SERVICE_CSV_ROW = dict(service_id=1, start_date=TODAY_DATE_STR, end_date=TODAY_DATE_STR, sunday=1, monday=0,
                            tuesday=0, wednesday=0, thursday=0, friday=0, saturday=0)
FULL_SERVICE_CSV_ROW = dict(service_id=1, start_date=TODAY_DATE_STR, end_date=TOMORROW_DATE_STR, sunday=1, monday=1,
                            tuesday=1, wednesday=1, thursday=1, friday=1, saturday=1, test_attribute="test data")
ALL_CSV_ROWS = [MINI_SERVICE_CSV_ROW, FULL_SERVICE_CSV_ROW]


class TestService(unittest.TestCase):
    def test_minimum_properties(self):
        td = TransitData()
        service = td.calendar.add(**MINI_SERVICE_CSV_ROW)

        self.assertTrue(hasattr(service, "id"))
        self.assertRaises(Exception, setattr, service, "id", "2")

        test_property(self, service, property_name="start_date", new_value=TOMORROW_DATE)
        test_property(self, service, property_name="end_date", new_value=TOMORROW_DATE)
        test_property(self, service, property_name="saturday", new_value=True)
        test_property(self, service, property_name="sunday", new_value=False)
        test_property(self, service, property_name="monday", new_value=True)
        test_property(self, service, property_name="tuesday", new_value=True)
        test_property(self, service, property_name="wednesday", new_value=True)
        test_property(self, service, property_name="thursday", new_value=True)
        test_property(self, service, property_name="friday", new_value=True)

    def test_maximum_properties(self):
        td = TransitData()
        service = td.calendar.add(**FULL_SERVICE_CSV_ROW)

        self.assertTrue(hasattr(service, "id"))
        self.assertRaises(Exception, setattr, service, "id", "2")

        test_property(self, service, property_name="start_date", new_value=TOMORROW_DATE)
        test_property(self, service, property_name="end_date", new_value=TOMORROW_DATE + timedelta(days=1))
        test_property(self, service, property_name="sunday", new_value=False)
        test_property(self, service, property_name="monday", new_value=False)
        test_property(self, service, property_name="tuesday", new_value=False)
        test_property(self, service, property_name="wednesday", new_value=False)
        test_property(self, service, property_name="thursday", new_value=False)
        test_property(self, service, property_name="friday", new_value=False)
        service.sunday = True
        test_property(self, service, property_name="saturday", new_value=False)

        self.assertIn("test_attribute", service.attributes)
        service.attributes["test_attribute"] = "new test data"
        self.assertEqual(service.attributes["test_attribute"], "new test data")

        self.assertNotIn("test_attribute2", service.attributes)
        service.attributes["test_attribute2"] = "more test data"
        self.assertEqual(service.attributes["test_attribute2"], "more test data")

    def test_get_csv_line(self):
        for row in ALL_CSV_ROWS:
            td = TransitData()
            service = td.calendar.add(**row)
            self.assertDictEqual(service.to_csv_line(), row)

    def test_get_csv_fields(self):
        for row in ALL_CSV_ROWS:
            td = TransitData()
            service = td.calendar.add(**row)
            self.assertListEqual(sorted(service.get_csv_fields()), sorted(row.keys()))

    def test_equal_operator(self):
        for row in ALL_CSV_ROWS:
            td1 = TransitData()
            td2 = TransitData()
            service1 = td1.calendar.add(**row)
            service2 = td2.calendar.add(**row)
            self.assertEqual(service1, service2)

    def test_not_equal_operator(self):
        original_td = TransitData()
        original_service = original_td.calendar.add(**FULL_SERVICE_CSV_ROW)

        new_td = TransitData()
        row = dict(FULL_SERVICE_CSV_ROW)
        row["service_id"] = 10
        edited_service = new_td.calendar.add(**row)
        self.assertNotEqual(original_service, edited_service)

        new_td = TransitData()
        edited_service = new_td.calendar.add(**FULL_SERVICE_CSV_ROW)
        edited_service.start_date = TOMORROW_DATE
        self.assertNotEqual(original_service, edited_service)

        new_td = TransitData()
        edited_service = new_td.calendar.add(**FULL_SERVICE_CSV_ROW)
        edited_service.end_date = TOMORROW_DATE + timedelta(days=1)
        self.assertNotEqual(original_service, edited_service)

        new_td = TransitData()
        edited_service = new_td.calendar.add(**FULL_SERVICE_CSV_ROW)
        edited_service.sunday = False
        self.assertNotEqual(original_service, edited_service)

        new_td = TransitData()
        edited_service = new_td.calendar.add(**FULL_SERVICE_CSV_ROW)
        edited_service.monday = False
        self.assertNotEqual(original_service, edited_service)

        new_td = TransitData()
        edited_service = new_td.calendar.add(**FULL_SERVICE_CSV_ROW)
        edited_service.tuesday = False
        self.assertNotEqual(original_service, edited_service)

        new_td = TransitData()
        edited_service = new_td.calendar.add(**FULL_SERVICE_CSV_ROW)
        edited_service.wednesday = False
        self.assertNotEqual(original_service, edited_service)

        new_td = TransitData()
        edited_service = new_td.calendar.add(**FULL_SERVICE_CSV_ROW)
        edited_service.thursday = False
        self.assertNotEqual(original_service, edited_service)

        new_td = TransitData()
        edited_service = new_td.calendar.add(**FULL_SERVICE_CSV_ROW)
        edited_service.friday = False
        self.assertNotEqual(original_service, edited_service)

        new_td = TransitData()
        edited_service = new_td.calendar.add(**FULL_SERVICE_CSV_ROW)
        edited_service.saturday = False
        self.assertNotEqual(original_service, edited_service)

        new_td = TransitData()
        edited_service = new_td.calendar.add(**FULL_SERVICE_CSV_ROW)
        edited_service.attributes["test_attribute"] = "new test data"
        self.assertNotEqual(original_service, edited_service)

        new_td = TransitData()
        edited_service = new_td.calendar.add(**FULL_SERVICE_CSV_ROW)
        edited_service.attributes["test_attribute2"] = "new test data"
        self.assertNotEqual(original_service, edited_service)


class TestServiceCollection(unittest.TestCase):
    def test_add(self):
        for row in ALL_CSV_ROWS:
            td = TransitData()
            service = td.calendar.add(**row)
            self.assertIn(service, td.calendar)

            self.assertIsInstance(service.id, int)
            self.assertEqual(service.id, row["service_id"])

            self.assertEqual(service.start_date.strftime("%Y%m%d"), row.get("start_date"))
            self.assertEqual(service.end_date.strftime("%Y%m%d"), row.get("end_date"))
            self.assertEqual(service.sunday, row.get("sunday"))
            self.assertEqual(service.monday, row.get("monday"))
            self.assertEqual(service.tuesday, row.get("tuesday"))
            self.assertEqual(service.wednesday, row.get("wednesday"))
            self.assertEqual(service.thursday, row.get("thursday"))
            self.assertEqual(service.friday, row.get("friday"))
            self.assertEqual(service.saturday, row.get("saturday"))
            self.assertEqual(service.attributes.get("test_attribute"), row.get("test_attribute"))

            self.assertEqual(len(service.attributes), len(row) - 10)

            self.assertRaises(Exception, td.calendar.add, **row)
            self.assertEqual(len(td.calendar), 1)

    def test_add_object(self):
        for row in ALL_CSV_ROWS:
            source_td = TransitData()
            dest_td = TransitData()

            source_service = source_td.calendar.add(**row)
            dest_service = dest_td.calendar.add_object(source_service)
            self.assertEqual(source_service, dest_service)

            services_num = len(dest_td.calendar)
            dest_td.calendar.add_object(source_service)
            self.assertEqual(services_num, len(dest_td.calendar))

            source_service.saturday = not source_service.saturday
            self.assertRaises(Exception, dest_td.calendar.add_object, source_service)

    def test_remove(self):
        td = TransitData()
        service = td.calendar.add(**FULL_SERVICE_CSV_ROW)
        self.assertIn(service, td.calendar)
        td.calendar.remove(service)
        self.assertNotIn(service, td.calendar)
        td.calendar.add(**FULL_SERVICE_CSV_ROW)
        self.assertIn(service, td.calendar)
        td.calendar.remove(service.id)
        self.assertNotIn(service, td.calendar)

    def test_clean(self):
        td = TransitData()
        td.calendar.add(**FULL_SERVICE_CSV_ROW)
        self.assertGreater(len(td.calendar), 0)
        td.calendar.clean()
        self.assertEqual(len(td.calendar), 0)

    # TODO: test load from file
