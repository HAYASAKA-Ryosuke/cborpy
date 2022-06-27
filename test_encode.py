import unittest
from encode import encode
import math


class TestEncode(unittest.TestCase):
    def test_encode(self):
        # floatについてはfloat64で解釈するのでRFCのexampleとずれる
        self.assertEqual(encode(0).hex(), "00")
        self.assertEqual(encode(1).hex(), "01")
        self.assertEqual(encode(10).hex(), "0a")
        self.assertEqual(encode(23).hex(), "17")
        self.assertEqual(encode(24).hex(), "1818")
        self.assertEqual(encode(25).hex(), "1819")
        self.assertEqual(encode(100).hex(), "1864")
        self.assertEqual(encode(1000).hex(), "1903e8")
        self.assertEqual(encode(1000000).hex(), "1a000f4240")
        self.assertEqual(encode(18446744073709551615).hex(), "1bffffffffffffffff")
        self.assertEqual(encode(-18446744073709551616).hex(), "3bffffffffffffffff")
        self.assertEqual(encode(-1).hex(), "20")
        self.assertEqual(encode(-10).hex(), "29")
        self.assertEqual(encode(-100).hex(), "3863")
        self.assertEqual(encode(-1000).hex(), "3903e7")
        self.assertEqual(encode(0.0).hex(), "fb0000000000000000")
        self.assertEqual(encode(-0.0).hex(), "fb8000000000000000")
        self.assertEqual(encode(1.0).hex(), "fb3ff0000000000000")
        self.assertEqual(encode(1.1).hex(), "fb3ff199999999999a")
        self.assertEqual(encode(1.1).hex(), "fb3ff199999999999a")
        self.assertEqual(encode(65504.0).hex(), "fb40effc0000000000")
        self.assertEqual(encode(100000.0).hex(), "fb40f86a0000000000")
        self.assertEqual(encode(3.4028234663852886e38).hex(), "fb47efffffe0000000")
        self.assertEqual(encode(1.0e300).hex(), "fb7e37e43c8800759c")
        self.assertEqual(encode(-4.0).hex(), "fbc010000000000000")
        self.assertEqual(encode(-4.1).hex(), "fbc010666666666666")
        self.assertEqual(encode(math.inf).hex(), "fb7ff0000000000000")
        self.assertEqual(encode(math.nan).hex(), "fb7ff8000000000000")
        self.assertEqual(encode(-math.inf).hex(), "fbfff0000000000000")
        self.assertEqual(encode(True).hex(), "f5")
        self.assertEqual(encode(False).hex(), "f4")
        self.assertEqual(encode(None).hex(), "f6")
        self.assertEqual(encode("").hex(), "60")
        self.assertEqual(encode("a").hex(), "6161")
        self.assertEqual(encode("IETF").hex(), "6449455446")
        self.assertEqual(encode('"\\').hex(), "62225c")
        self.assertEqual(encode([]).hex(), "80")
        self.assertEqual(encode([1, 2, 3]).hex(), "83010203")
        self.assertEqual(encode([1, [2, 3], [4, 5]]).hex(), "8301820203820405")
        self.assertEqual(
            encode({"a": 1, "b": [1, 2], "c": 1.1}).hex(),
            "a361610161628201026163fb3ff199999999999a",
        )


if __name__ == "__main__":
    unittest.main()
