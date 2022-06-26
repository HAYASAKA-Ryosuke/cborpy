import unittest
from decode import decode


class TestDecode(unittest.TestCase):
    def test_decode(self):
        self.assertEqual(decode("00"), 0)
        self.assertEqual(decode("01"), 1)
        self.assertEqual(decode("0a"), 10)
        self.assertEqual(decode("17"), 23)
        self.assertEqual(decode("1818"), 24)
        self.assertEqual(decode("1819"), 25)
        self.assertEqual(
            decode("8A05251401020304050607"), [5, -6, 20, 1, 2, 3, 4, 5, 6, 7]
        )


if __name__ == "__main__":
    unittest.main()
