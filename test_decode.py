import unittest
from decode import decode


class TestDecode(unittest.TestCase):
    def test_decode(self):
        self.assertEqual(decode(b'\x00'), 0)
        self.assertEqual(decode(b'\x01'), 1)
        self.assertEqual(decode(b'\x0a'), 10)
        self.assertEqual(decode(b'\x17'), 23)
        self.assertEqual(decode(b'\x18\x18'), 24)
        self.assertEqual(decode(b'\x18\x19'), 25)
        self.assertEqual(decode(b'\x8A\x05\x25\x14\x01\x02\x03\x04\x05\x06\x07'), [5, -6, 20, 1, 2, 3, 4, 5, 6, 7])

if __name__ == "__main__":
    unittest.main()
