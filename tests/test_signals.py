import unittest
from src.signals import ChatStats, calculate


class TestSignals(unittest.TestCase):
    def _stats(self, **overrides):
        defaults = dict(
            your_msgs=10,
            their_msgs=10,
            your_avg_len=50,
            their_avg_len=50,
            your_questions=3,
            their_questions=3,
            their_avg_reply_minutes=20,
            their_initiations=2,
            consecutive_short_replies=0,
        )
        defaults.update(overrides)
        return ChatStats(**defaults)

    def test_balanced_conversation_is_green(self):
        result = calculate(self._stats())
        self.assertEqual(result.zone, "green")

    def test_one_sided_long_msgs_drops_to_yellow_or_red(self):
        result = calculate(self._stats(your_avg_len=200, their_avg_len=20))
        self.assertIn(result.zone, ("yellow", "red"))

    def test_no_questions_back_drops_score(self):
        result = calculate(self._stats(their_questions=0))
        balanced = calculate(self._stats())
        self.assertLess(result.score, balanced.score)

    def test_short_streak_pushes_red(self):
        result = calculate(self._stats(
            their_avg_len=10,
            their_questions=0,
            consecutive_short_replies=4,
            their_avg_reply_minutes=600,
            their_initiations=0,
        ))
        self.assertEqual(result.zone, "red")

    def test_factors_in_output(self):
        result = calculate(self._stats())
        d = result.to_dict()
        self.assertIn("length_ratio", d["factors"])
        self.assertIn("questions_back", d["factors"])
        self.assertIn("recent_trend", d["factors"])


if __name__ == "__main__":
    unittest.main()
