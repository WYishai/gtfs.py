def test_property(test_case, obj, property_name, new_value):
    test_case.assertTrue(hasattr(obj, property_name))
    test_case.assertNotEqual(getattr(obj, property_name), new_value)
    setattr(obj, property_name, new_value)
    test_case.assertEqual(getattr(obj, property_name), new_value)


def test_attribute(test_case, obj, attribute_name, new_value):
    obj.attributes[attribute_name] = new_value
    test_case.assertEqual(obj.attributes[attribute_name], new_value)
