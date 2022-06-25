import io
import struct
import convert_byte
import math


def decode(value: bytes):
    decoder = Decoder()
    return decoder.decode(value)

class Decoder:
    def get_major(self, value: bytes):
        return value[0] >> 5

    def decode(self, value):
        major = self.get_major(value)
        if major == 0:
            return self.decode_int(value)
        elif major == 1:
            return self.decode_int(value, True)
        elif major == 4:
            return self.decode_list(value)

    def decode_int(self, value: bytes, is_negative: bool=False):
        if value[0] & 0x1F >= 24:
            result = int.from_bytes(value[1:], 'big')
        else:
            result = int.from_bytes(value, 'big') & 0x1F

        if is_negative:
            return -(result + 1)

        return result

    def decode_list(self, values: list):
        length = 0
        pad = 0
        if values[0] & 0x1F < 24:
            pad = 0
            length = values[0] & 0x1F
        if values[0] & 0x1F == 24:
            pad = 1
            length = values[0:1] & 0x1F
        if values[0] & 0x1F == 25:
            pad = 2
            length = values[0:2] & 0x1F
        if values[0] & 0x1F == 26:
            pad = 3
            length = values[0:3] & 0x1F
        if values[0] & 0x1F == 27:
            pad = 4
            length = values[0:4] & 0x1F
        result = []
        for i in range(length):
            result.append(self.decode(int.to_bytes(values[pad + 1 + i], 1, 'big')))
        return result
