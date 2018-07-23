import unittest

from gtfspy import TransitData
from test_utils.test_case_utils import test_property

MINI_AGENCY_CSV_ROW = dict(agency_id=1, agency_name="agency name", agency_url="http://www.agencyname.com/",
                           agency_timezone="Asia/Jerusalem")
FULL_AGENCY_CSV_ROW = dict(agency_id=1, agency_name="agency name", agency_url="http://www.agencyname.com/",
                           agency_timezone="Asia/Jerusalem", agency_lang="HE", agency_phone="+972-2-1234567",
                           agency_email="mail@agencyname.com", agency_fare_url="http://www.agencyname.com/fare",
                           test_attribute="test data")
ALL_CSV_ROWS = [MINI_AGENCY_CSV_ROW, FULL_AGENCY_CSV_ROW]


class TestAgency(unittest.TestCase):
    def test_minimum_properties(self):
        td = TransitData()
        agency = td.agencies.add(**MINI_AGENCY_CSV_ROW)

        self.assertTrue(hasattr(agency, "id"))
        self.assertRaises(Exception, setattr, agency, "id", 2)

        test_property(self, agency, property_name="agency_name", new_value="test name")
        test_property(self, agency, property_name="agency_url", new_value="http://testurl.com/")
        test_property(self, agency, property_name="agency_timezone", new_value="Asia/Hebron")
        test_property(self, agency, property_name="agency_lang", new_value="HE")
        test_property(self, agency, property_name="agency_phone", new_value="*1234")
        test_property(self, agency, property_name="agency_email", new_value="mail@agencyname.com")
        test_property(self, agency, property_name="agency_fare_url", new_value="http://testurl.com/fare/")

    def test_maximum_properties(self):
        td = TransitData()
        agency = td.agencies.add(**FULL_AGENCY_CSV_ROW)

        self.assertTrue(hasattr(agency, "id"))
        self.assertRaises(Exception, setattr, agency, "id", 2)

        test_property(self, agency, property_name="agency_name", new_value="test name")
        test_property(self, agency, property_name="agency_url", new_value="http://testurl.com/")
        test_property(self, agency, property_name="agency_timezone", new_value="Asia/Hebron")
        test_property(self, agency, property_name="agency_lang", new_value="EN")
        test_property(self, agency, property_name="agency_phone", new_value="*1234")
        test_property(self, agency, property_name="agency_email", new_value="mail2@agencyname.com")
        test_property(self, agency, property_name="agency_fare_url", new_value="http://testurl.com/fare/")

        self.assertIn("test_attribute", agency.attributes)
        agency.attributes["test_attribute"] = "new test data"
        self.assertEqual(agency.attributes["test_attribute"], "new test data")

        self.assertNotIn("test_attribute2", agency.attributes)
        agency.attributes["test_attribute2"] = "more test data"
        self.assertEqual(agency.attributes["test_attribute2"], "more test data")

    def test_get_csv_line(self):
        for row in ALL_CSV_ROWS:
            td = TransitData()
            agency = td.agencies.add(**row)
            self.assertDictEqual(agency.to_csv_line(), row)

    def test_get_csv_fields(self):
        for row in ALL_CSV_ROWS:
            td = TransitData()
            agency = td.agencies.add(**row)
            self.assertListEqual(sorted(agency.get_csv_fields()), sorted(row.iterkeys()))

    def test_equal_operator(self):
        for row in ALL_CSV_ROWS:
            td1 = TransitData()
            td2 = TransitData()
            agency1 = td1.agencies.add(**row)
            agency2 = td2.agencies.add(**row)
            self.assertEqual(agency1, agency2)

    def test_not_equal_operator(self):
        original_td = TransitData()
        original_agency = original_td.agencies.add(**FULL_AGENCY_CSV_ROW)

        new_td = TransitData()
        row = dict(FULL_AGENCY_CSV_ROW)
        row["agency_id"] = 10
        edited_agency = new_td.agencies.add(**row)
        self.assertNotEqual(original_agency, edited_agency)

        new_td = TransitData()
        edited_agency = new_td.agencies.add(**FULL_AGENCY_CSV_ROW)
        edited_agency.agency_name = "new name"
        self.assertNotEqual(original_agency, edited_agency)

        new_td = TransitData()
        edited_agency = new_td.agencies.add(**FULL_AGENCY_CSV_ROW)
        edited_agency.agency_url = "http://newurl.com/"
        self.assertNotEqual(original_agency, edited_agency)

        new_td = TransitData()
        edited_agency = new_td.agencies.add(**FULL_AGENCY_CSV_ROW)
        edited_agency.agency_timezone = "Asia/Hebron"
        self.assertNotEqual(original_agency, edited_agency)

        new_td = TransitData()
        edited_agency = new_td.agencies.add(**FULL_AGENCY_CSV_ROW)
        edited_agency.agency_lang = "EN"
        self.assertNotEqual(original_agency, edited_agency)

        new_td = TransitData()
        edited_agency = new_td.agencies.add(**FULL_AGENCY_CSV_ROW)
        edited_agency.agency_phone = "*1234"
        self.assertNotEqual(original_agency, edited_agency)

        new_td = TransitData()
        edited_agency = new_td.agencies.add(**FULL_AGENCY_CSV_ROW)
        edited_agency.agency_email = "newmail@host.com"
        self.assertNotEqual(original_agency, edited_agency)

        new_td = TransitData()
        edited_agency = new_td.agencies.add(**FULL_AGENCY_CSV_ROW)
        edited_agency.agency_fare_url = "http://newurl/fare"
        self.assertNotEqual(original_agency, edited_agency)

        new_td = TransitData()
        edited_agency = new_td.agencies.add(**FULL_AGENCY_CSV_ROW)
        edited_agency.attributes["test_attribute"] = "new test data"
        self.assertNotEqual(original_agency, edited_agency)

        new_td = TransitData()
        edited_agency = new_td.agencies.add(**FULL_AGENCY_CSV_ROW)
        edited_agency.attributes["test_attribute2"] = "new test data"
        self.assertNotEqual(original_agency, edited_agency)


class TestAgencyCollection(unittest.TestCase):
    def test_add(self):
        for row in ALL_CSV_ROWS:
            td = TransitData()
            agency = td.agencies.add(**row)
            self.assertIn(agency, td.agencies)

            self.assertIsInstance(agency.id, int)
            self.assertEqual(agency.id, row["agency_id"])

            self.assertEqual(agency.agency_name, row.get("agency_name"))
            self.assertEqual(agency.agency_url, row.get("agency_url"))
            self.assertEqual(agency.agency_timezone, row.get("agency_timezone"))
            self.assertEqual(agency.agency_lang, row.get("agency_lang"))
            self.assertEqual(agency.agency_phone, row.get("agency_phone"))
            self.assertEqual(agency.agency_email, row.get("agency_email"))
            self.assertEqual(agency.agency_fare_url, row.get("agency_fare_url"))
            self.assertEqual(agency.attributes.get("test_attribute"), row.get("test_attribute"))

            self.assertEqual(len(agency.attributes), len(row) - 4)

            self.assertRaises(Exception, td.agencies.add, **row)
            self.assertEqual(len(td.agencies), 1)

    def test_add_object(self):
        for row in ALL_CSV_ROWS:
            source_td = TransitData()
            dest_td = TransitData()

            source_agency = source_td.agencies.add(**row)
            dest_agency = dest_td.agencies.add_object(source_agency)
            self.assertEqual(source_agency, dest_agency)

            agencies_num = len(dest_td.agencies)
            dest_td.agencies.add_object(source_agency)
            self.assertEqual(agencies_num, len(dest_td.agencies))

            source_agency.agency_name = "agency new name"
            self.assertRaises(Exception, dest_td.agencies.add_object, source_agency)

    def test_remove(self):
        td = TransitData()
        agency = td.agencies.add(**FULL_AGENCY_CSV_ROW)
        self.assertIn(agency, td.agencies)
        td.agencies.remove(agency)
        self.assertNotIn(agency, td.agencies)
        td.agencies.add(**FULL_AGENCY_CSV_ROW)
        self.assertIn(agency, td.agencies)
        td.agencies.remove(agency.id)
        self.assertNotIn(agency, td.agencies)

    def test_clean(self):
        td = TransitData()
        td.agencies.add(**FULL_AGENCY_CSV_ROW)
        self.assertGreater(len(td.agencies), 0)
        td.agencies.clean()
        self.assertEqual(len(td.agencies), 0)

    # TODO: test load from file
