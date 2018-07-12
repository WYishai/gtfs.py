import sys
import unittest

from gtfspy.utils.parsing import *


class TestStrToBool(unittest.TestCase):
    def test_true_string(self):
        self.assertTrue(str_to_bool("1"))
        self.assertTrue(str_to_bool("2"))
        self.assertTrue(str_to_bool("-1"))
        self.assertTrue(str_to_bool(str(sys.maxint)))

    def test_false_string(self):
        self.assertFalse(str_to_bool(0))


class TestParseOrDefault(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse_or_default("1", None, int), 1)
        self.assertEqual(parse_or_default(1, None, str), "1")
        self.assertEqual(parse_or_default("1", None, str_to_bool), True)
        self.assertEqual(parse_or_default("aaaa", None, lambda x: True), True)

    def test_default(self):
        self.assertEqual(parse_or_default(None, 8, int), 8)
        self.assertEqual(parse_or_default(None, 8, str), 8)
        self.assertEqual(parse_or_default(None, 8, str_to_bool), 8)
        self.assertEqual(parse_or_default(None, 8, lambda x: True), 8)


class TestYesNoUnknownParser(unittest.TestCase):
    def test_parse_int_to_bool(self):
        self.assertIsNone(parse_yes_no_unknown(0))
        self.assertTrue(parse_yes_no_unknown(1))
        self.assertFalse(parse_yes_no_unknown(2))

        self.assertIsNone(parse_yes_no_unknown(3))
        self.assertIsNone(parse_yes_no_unknown(-1))
        self.assertIsNone(parse_yes_no_unknown(100))
        self.assertIsNone(parse_yes_no_unknown(sys.maxint))

    def test_parse_bool_to_int(self):
        self.assertIn(yes_no_unknown_to_int(None), [None, 0])
        self.assertEqual(yes_no_unknown_to_int(True), 1)
        self.assertEqual(yes_no_unknown_to_int(False), 2)
