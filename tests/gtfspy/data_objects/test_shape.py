import unittest

from gtfspy import TransitData
from test_utils.test_case_utils import test_property

MINI_SHAPE_CSV_ROWS = [dict(shape_id=1, shape_pt_lat=31.789467, shape_pt_lon=35.203715, shape_pt_sequence=0),
                       dict(shape_id=1, shape_pt_lat=32.055818, shape_pt_lon=34.779427, shape_pt_sequence=1)]
FULL_SHAPE_CSV_ROWS = [dict(shape_id=1, shape_pt_lat=-31.789467, shape_pt_lon=-35.203715, shape_pt_sequence=0,
                            shape_dist_traveled=0),
                       dict(shape_id=1, shape_pt_lat=-32.055818, shape_pt_lon=-34.779427, shape_pt_sequence=1,
                            shape_dist_traveled=60.0, test_attribute="test data")]
ALL_CSV_ROWS = [MINI_SHAPE_CSV_ROWS, FULL_SHAPE_CSV_ROWS]


class TestShape(unittest.TestCase):
    def test_minimum_properties(self):
        td = TransitData()
        shape_point = None
        for row in MINI_SHAPE_CSV_ROWS:
            shape_point = td.shapes.add(**row)

        shape = iter(td.shapes).next()
        self.assertTrue(hasattr(shape, "id"))
        self.assertRaises(Exception, setattr, shape, "id", "2")

        test_property(self, shape_point, property_name="latitude", new_value=0)
        test_property(self, shape_point, property_name="longitude", new_value=0)
        test_property(self, shape_point, property_name="sequence", new_value=2)
        test_property(self, shape_point, property_name="shape_dist_traveled", new_value=60.2)

    def test_maximum_properties(self):
        td = TransitData()
        shape_point = None
        for row in FULL_SHAPE_CSV_ROWS:
            shape_point = td.shapes.add(**row)

        shape = iter(td.shapes).next()
        self.assertTrue(hasattr(shape, "id"))
        self.assertRaises(Exception, setattr, shape, "id", "2")

        test_property(self, shape_point, property_name="latitude", new_value=0)
        test_property(self, shape_point, property_name="longitude", new_value=0)
        test_property(self, shape_point, property_name="sequence", new_value=2)
        test_property(self, shape_point, property_name="shape_dist_traveled", new_value=60.2)

        self.assertIn("test_attribute", shape_point.attributes)
        shape_point.attributes["test_attribute"] = "new test data"
        self.assertEqual(shape_point.attributes["test_attribute"], "new test data")

        self.assertNotIn("test_attribute2", shape_point.attributes)
        shape_point.attributes["test_attribute2"] = "more test data"
        self.assertEqual(shape_point.attributes["test_attribute2"], "more test data")

    def test_get_csv_line(self):
        for rows in ALL_CSV_ROWS:
            td = TransitData()
            for row in rows:
                td.shapes.add(**row)
            shape = iter(td.shapes).next()
            self.assertListEqual(list(shape.to_csv_line()), rows)

    def test_get_csv_fields(self):
        for rows in ALL_CSV_ROWS:
            td = TransitData()
            for row in rows:
                td.shapes.add(**row)
            shape = iter(td.shapes).next()
            self.assertListEqual(sorted(shape.get_csv_fields()),
                                 sorted(list({key for row in rows for key in row.iterkeys()})))

    def test_equal_operator(self):
        for rows in ALL_CSV_ROWS:
            td1 = TransitData()
            td2 = TransitData()
            for row in rows:
                shape_point1 = td1.shapes.add(**row)
                shape_point2 = td2.shapes.add(**row)
                self.assertEqual(shape_point1, shape_point2)
            self.assertEqual(iter(td1.shapes).next(), iter(td2.shapes).next())

    def test_not_equal_operator(self):
        original_td = TransitData()
        for row in FULL_SHAPE_CSV_ROWS:
            original_td.shapes.add(**row)

        new_td = TransitData()
        rows = [dict(row) for row in FULL_SHAPE_CSV_ROWS]
        for row in rows:
            row["shape_id"] = 10
        for row, original_shape_point in zip(rows, iter(original_td.shapes).next().shape_points):
            new_td.shapes.add(**row)
        self.assertNotEqual(iter(original_td.shapes).next(), iter(new_td.shapes).next())

        new_td = TransitData()
        for row, original_shape_point in zip(FULL_SHAPE_CSV_ROWS, iter(original_td.shapes).next().shape_points):
            edited_shape_point = new_td.shapes.add(**row)
            edited_shape_point.latitude = 0
            self.assertNotEqual(original_shape_point, edited_shape_point)
        self.assertNotEqual(iter(original_td.shapes).next(), iter(new_td.shapes).next())

        new_td = TransitData()
        for row, original_shape_point in zip(FULL_SHAPE_CSV_ROWS, iter(original_td.shapes).next().shape_points):
            edited_shape_point = new_td.shapes.add(**row)
            edited_shape_point.longitude = 0
            self.assertNotEqual(original_shape_point, edited_shape_point)
        self.assertNotEqual(iter(original_td.shapes).next(), iter(new_td.shapes).next())

        new_td = TransitData()
        for row, original_shape_point in zip(FULL_SHAPE_CSV_ROWS, iter(original_td.shapes).next().shape_points):
            edited_shape_point = new_td.shapes.add(**row)
            edited_shape_point.sequence += 1
            self.assertNotEqual(original_shape_point, edited_shape_point)
        self.assertNotEqual(iter(original_td.shapes).next(), iter(new_td.shapes).next())

        new_td = TransitData()
        for row, original_shape_point in zip(FULL_SHAPE_CSV_ROWS, iter(original_td.shapes).next().shape_points):
            edited_shape_point = new_td.shapes.add(**row)
            edited_shape_point.shape_dist_traveled = 62.2
            self.assertNotEqual(original_shape_point, edited_shape_point)
        self.assertNotEqual(iter(original_td.shapes).next(), iter(new_td.shapes).next())

        new_td = TransitData()
        for row, original_shape_point in zip(FULL_SHAPE_CSV_ROWS, iter(original_td.shapes).next().shape_points):
            edited_shape_point = new_td.shapes.add(**row)
            edited_shape_point.attributes["test_attribute"] = "new test data"
            self.assertNotEqual(original_shape_point, edited_shape_point)
        self.assertNotEqual(iter(original_td.shapes).next(), iter(new_td.shapes).next())


class TestShapeCollection(unittest.TestCase):
    def test_add(self):
        for rows in ALL_CSV_ROWS:
            td = TransitData()
            for row in rows:
                shape_point = td.shapes.add(**row)

                self.assertEqual(shape_point.latitude, row.get("shape_pt_lat"))
                self.assertEqual(shape_point.longitude, row.get("shape_pt_lon"))
                self.assertEqual(shape_point.sequence, row.get("shape_pt_sequence"))
                self.assertEqual(shape_point.shape_dist_traveled, row.get("shape_dist_traveled"))
                self.assertEqual(shape_point.attributes.get("test_attribute"), row.get("test_attribute"))

                self.assertEqual(len(shape_point.attributes), len(row) - 4)

                # self.assertRaises(Exception, td.shapes.add, **row)
                self.assertEqual(len(td.shapes), 1)

            shape_id = rows[-1]["shape_id"]
            shape = td.shapes[shape_id]
            self.assertIn(shape, td.shapes)

            self.assertIsInstance(shape.id, int)
            self.assertEqual(shape.id, shape_id)

    def test_add_object(self):
        for rows in ALL_CSV_ROWS:
            source_td = TransitData()
            dest_td = TransitData()

            for row in rows:
                source_td.shapes.add(**row)
            source_shape = iter(source_td.shapes).next()
            dest_shape = dest_td.shapes.add_object(source_shape, recursive=True)
            self.assertEqual(source_shape, dest_shape)

            shapes_num = len(dest_td.shapes)
            dest_td.shapes.add_object(source_shape)
            self.assertEqual(shapes_num, len(dest_td.shapes))

            source_shape.shape_points[-1].sequence += 1
            self.assertRaises(Exception, dest_td.shapes.add_object, source_shape)

    def test_remove(self):
        td = TransitData()
        for row in FULL_SHAPE_CSV_ROWS:
            td.shapes.add(**row)
        shape_id = FULL_SHAPE_CSV_ROWS[-1]["shape_id"]
        self.assertIn(shape_id, td.shapes)
        td.shapes.remove(td.shapes[shape_id], clean_after=False)
        self.assertNotIn(shape_id, td.shapes)
        for row in FULL_SHAPE_CSV_ROWS:
            td.shapes.add(**row)
        self.assertIn(shape_id, td.shapes)
        td.shapes.remove(shape_id)
        self.assertNotIn(shape_id, td.shapes)

    def test_clean(self):
        td = TransitData()
        for row in FULL_SHAPE_CSV_ROWS:
            td.shapes.add(**row)
        self.assertGreater(len(td.shapes), 0)
        td.shapes.clean()
        self.assertEqual(len(td.shapes), 0)

    # TODO: test load from file
