import unittest
from src.analyzer import analyze


class TestAnalyzer(unittest.TestCase):
    def test_clean_message_scores_green(self):
        result = analyze("เมื่อกี้คลาสสนุกมาก สัปดาห์หน้าจะไปต่อไหม?")
        self.assertEqual(result.verdict, "green")
        self.assertEqual(len(result.flags), 0)
        self.assertLess(result.pushiness, 0.4)

    def test_guilt_trip_flagged_red(self):
        result = analyze("ทำไมไม่ทักมาบ้าง")
        self.assertEqual(result.verdict, "red")
        self.assertGreaterEqual(len(result.flags), 1)
        self.assertEqual(result.flags[0].category, "guilt_trip")

    def test_english_guilt_trip(self):
        result = analyze("why aren't you replying??")
        self.assertEqual(result.verdict, "red")
        categories = {f.category for f in result.flags}
        self.assertIn("guilt_trip", categories)

    def test_passive_aggressive_miss(self):
        result = analyze("คิดถึงจังเลย ทำไมไม่ทักมาบ้าง")
        self.assertIn(result.verdict, ("yellow", "red"))
        self.assertGreater(len(result.flags), 0)

    def test_desperation_punctuation(self):
        result = analyze("hello???")
        categories = {f.category for f in result.flags}
        self.assertIn("desperation", categories)

    def test_demanding_reply(self):
        result = analyze("answer me please")
        categories = {f.category for f in result.flags}
        self.assertIn("demanding", categories)

    def test_length_warning(self):
        long_msg = "หวัดดี " * 100
        result = analyze(long_msg)
        self.assertIsNotNone(result.length_warning)

    def test_serializable_to_dict(self):
        result = analyze("ทำไมไม่ตอบ")
        d = result.to_dict()
        self.assertIn("pushiness", d)
        self.assertIn("verdict", d)
        self.assertIn("flags", d)
        self.assertIsInstance(d["flags"], list)


if __name__ == "__main__":
    unittest.main()
