import unittest

from gtfspy.data_objects import Translator


class TestTranslator(unittest.TestCase):
    def test_translate(self):
        translator = Translator()
        translator.add_translate("EN", "hello", "hello")
        translator.add_translate("IT", "hello", "ciao")
        translator.add_translate("GR", "hello", "hallo")
        translator.add_translate("NE", "hello", "hallo")
        translator.add_translate("FR", "hello", "bonjour")
        translator.add_translate("EN", "bye", "bye")
        translator.add_translate("IT", "bye", "addio")
        translator.add_translate("NE", "bye", "doei")
        translator.add_translate("FR", "bye", "au revoir")
        translator.add_translate("EN", "test", "test")

        self.assertIsNone(translator.translate("moses", "HE"))
        self.assertIsNone(translator.translate("moses", "EN"))

        self.assertEqual(translator.translate("hello", "EN"), "hello")
        self.assertEqual(translator.translate("hello", "IT"), "ciao")
        self.assertEqual(translator.translate("hello", "GR"), "hallo")
        self.assertEqual(translator.translate("hello", "NE"), "hallo")

        self.assertEqual(translator.translate("bye", "EN"), "bye")
        self.assertEqual(translator.translate("bye", "IT"), "addio")
        self.assertEqual(translator.translate("bye", "NE"), "doei")
        self.assertEqual(translator.translate("bye", "FR"), "au revoir")
        self.assertIsNone(translator.translate("bye", "GR"))

        self.assertEqual(translator.translate("test", "EN"), "test")
        self.assertIsNone(translator.translate("test", "FR"))

        self.assertEqual(translator.try_translate("hello", "IT"), "ciao")
        self.assertEqual(translator.try_translate("test", "GR"), "test")
