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
        self.assertTrue(decode("f5"))
        self.assertFalse(decode("f4"))
        self.assertIsNone(decode("f6"))
        self.assertEqual(decode("fb0000000000000000"), 0.0)
        self.assertEqual(decode("fb8000000000000000"), -0.0)
        self.assertEqual(decode("fb3ff199999999999a"), 1.1)
        self.assertEqual(decode("fb40effc0000000000"), 65504.0)
        self.assertEqual(decode("fb40f86a0000000000"), 100000.0)
        self.assertEqual(decode("fb47efffffe0000000"), 3.4028234663852886e38)
        self.assertEqual(decode("fb7e37e43c8800759c"), 1.0e300)
        self.assertEqual(decode("fbc010000000000000"), -4.0)
        self.assertEqual(decode("fbc010666666666666"), -4.1)


if __name__ == "__main__":
    unittest.main()
