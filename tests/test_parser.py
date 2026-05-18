import unittest
from src.parser import parse_chat


class TestParser(unittest.TestCase):
    def test_basic_parsing(self):
        raw = """Me: hi
Her: hey what's up
Me: how was your weekend?
Her: pretty good
"""
        stats = parse_chat(raw)
        self.assertEqual(stats.your_msgs, 2)
        self.assertEqual(stats.their_msgs, 2)
        self.assertEqual(stats.your_questions, 1)
        self.assertEqual(stats.their_questions, 0)

    def test_thai_speakers(self):
        raw = """เรา: สบายดีไหม
เขา: ก็เรื่อยๆ
เรา: ไปกินข้าวมารึยัง
เขา: ยังเลย
"""
        stats = parse_chat(raw)
        self.assertEqual(stats.your_msgs, 2)
        self.assertEqual(stats.their_msgs, 2)
        self.assertEqual(stats.your_questions, 2)

    def test_question_detection_thai(self):
        raw = """Me: สบายดีไหม
Her: ดี
"""
        stats = parse_chat(raw)
        self.assertEqual(stats.your_questions, 1)

    def test_consecutive_short_replies_detected(self):
        raw = """Me: เป็นไงบ้างช่วงนี้ ทำอะไรอยู่
Her: ก็เรื่อยๆ
Me: ที่ทำงานเป็นไง
Her: ปกติ
Me: งั้นวันหยุดทำอะไร
Her: นอน
"""
        stats = parse_chat(raw)
        self.assertGreaterEqual(stats.consecutive_short_replies, 3)
        self.assertLess(stats.their_avg_len, stats.your_avg_len)

    def test_empty_chat_does_not_crash(self):
        stats = parse_chat("")
        self.assertEqual(stats.your_msgs, 0)
        self.assertEqual(stats.their_msgs, 0)


if __name__ == "__main__":
    unittest.main()
