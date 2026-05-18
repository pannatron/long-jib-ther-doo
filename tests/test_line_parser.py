import unittest
from src.line_parser import parse_line_export


SAMPLE_LINE_EXPORT = """[LINE] Chat with Nong
Saved on: 2024/05/15 14:30

2024/05/10 (Fri)
10:23\tNong\tหวัดดี เป็นไงบ้าง
10:25\tMe\tสบายดี วันนี้ทำอะไรอยู่
11:00\tNong\tไปกินข้าวกับเพื่อน

2024/05/11 (Sat)
09:15\tMe\tเมื่อคืนสนุกไหม
14:30\tNong\tก็โอเค
14:31\tMe\tเสาร์นี้ว่างไหม
20:00\tNong\tไม่ค่อยว่าง
"""


SAMPLE_WITH_STICKERS = """2024/05/10 (Fri)
10:00\tMe\tหวัดดี
10:05\tNong\t[Sticker]
10:06\tNong\tเป็นไงบ้าง
10:10\tMe\t[Photo]
"""


SAMPLE_THAI_ALIAS = """2024/05/10 (Fri)
10:00\tฉัน\tหวัดดี
10:05\tNong\tเป็นไงบ้าง
"""


class TestLineParser(unittest.TestCase):
    def test_basic_export_counts_messages(self):
        stats = parse_line_export(SAMPLE_LINE_EXPORT)
        self.assertEqual(stats.your_msgs, 3)
        self.assertEqual(stats.their_msgs, 4)

    def test_questions_detected(self):
        stats = parse_line_export(SAMPLE_LINE_EXPORT)
        self.assertGreaterEqual(stats.your_questions, 2)

    def test_reply_gaps_computed_across_days(self):
        stats = parse_line_export(SAMPLE_LINE_EXPORT)
        self.assertGreater(stats.their_avg_reply_minutes, 0)

    def test_stickers_and_photos_skipped(self):
        stats = parse_line_export(SAMPLE_WITH_STICKERS)
        self.assertEqual(stats.your_msgs, 1)
        self.assertEqual(stats.their_msgs, 1)

    def test_thai_alias_recognized(self):
        stats = parse_line_export(SAMPLE_THAI_ALIAS)
        self.assertEqual(stats.your_msgs, 1)
        self.assertEqual(stats.their_msgs, 1)

    def test_custom_your_name(self):
        custom = """2024/05/10 (Fri)
10:00\tSongkarn\tหวัดดี
10:05\tNong\tเป็นไงบ้าง
"""
        stats = parse_line_export(custom, your_name="Songkarn")
        self.assertEqual(stats.your_msgs, 1)
        self.assertEqual(stats.their_msgs, 1)

    def test_empty_input(self):
        stats = parse_line_export("")
        self.assertEqual(stats.your_msgs, 0)
        self.assertEqual(stats.their_msgs, 0)

    def test_short_streak_detected(self):
        chat = """2024/05/10 (Fri)
10:00\tMe\tเป็นไงบ้างช่วงนี้ ทำงานหนักไหม
10:05\tNong\tก็โอเค
10:10\tMe\tอยากไปกินข้าวด้วยกันไหม
10:20\tNong\tไม่ว่าง
10:30\tMe\tงั้นวันเสาร์ดีไหม
10:35\tNong\tดูก่อน
"""
        stats = parse_line_export(chat)
        self.assertGreaterEqual(stats.consecutive_short_replies, 3)


if __name__ == "__main__":
    unittest.main()
