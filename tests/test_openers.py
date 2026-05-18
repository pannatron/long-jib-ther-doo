import unittest
from src.openers import suggest, list_categories


class TestOpeners(unittest.TestCase):
    def test_list_categories_returns_all(self):
        cats = list_categories()
        self.assertGreater(len(cats), 0)
        for c in cats:
            self.assertIn("id", c)
            self.assertIn("label_th", c)
            self.assertIn("label_en", c)

    def test_suggest_class_workshop(self):
        result = suggest("class_workshop")
        self.assertEqual(result.category, "class_workshop")
        self.assertGreater(len(result.openers), 0)
        for opener in result.openers:
            self.assertTrue(opener.th)
            self.assertTrue(opener.en)
            self.assertTrue(opener.intent)

    def test_unknown_category_raises(self):
        with self.assertRaises(KeyError):
            suggest("nonexistent_category_xyz")

    def test_gym_yoga_has_warning(self):
        result = suggest("gym_yoga_studio")
        self.assertIsNotNone(result.warning_th)
        self.assertIsNotNone(result.warning_en)

    def test_universal_dont_present(self):
        result = suggest("class_workshop")
        self.assertIsNotNone(result.universal_dont)
        self.assertGreater(len(result.universal_dont), 0)


if __name__ == "__main__":
    unittest.main()
