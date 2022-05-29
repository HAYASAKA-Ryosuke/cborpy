import io
import struct
import convert_byte
import math


def encode(value):
    buff = io.BytesIO()
    encoder = Encoder(buff)
    encoder.encode(value)
    return encoder.result()


class Encoder:
    def __init__(self, buff):
        self.buff = buff

    def result(self):
        return self.buff.getvalue()

    def encode(self, value):
        if isinstance(value, bool):
            self.encode_bool(value)
        elif value is None:
            self.encode_none()
        elif isinstance(value, int):
            self.encode_int(value)
        elif isinstance(value, float):
            self.encode_float(value)
        elif isinstance(value, str):
            self.encode_str(value)
        elif isinstance(value, list):
            self.encode_list(value)
        elif isinstance(value, dict):
            self.encode_dict(value)

    def encode_int(self, value: int):
        if value >= 0:
            major = 0
            self.buff.write(convert_byte.encode_byte(major, value))
        else:
            major = 1
            value = -1 * value - 1
            self.buff.write(convert_byte.encode_byte(major, value))

    def encode_list(self, values: list):
        major = 4
        self.buff.write(convert_byte.encode_byte(major, len(values)))
        for value in values:
            self.encode(value)

    def encode_float(self, value: float):
        major = 7
        # 25,26、および27の5ビット値は、16ビット、32ビット、および64ビットに割り振られている。python3はfloat64なので27
        fivebit_value = 27
        # >: big endian, B: unsigned char(byte), d: double
        self.buff.write(struct.pack(">Bd", (major << 5) | fivebit_value, value))

    def encode_str(self, value: str):
        major = 3
        self.buff.write(convert_byte.encode_byte(major, len(value)))
        self.buff.write(value.encode())

    def encode_dict(self, items: dict):
        major = 5
        self.buff.write(convert_byte.encode_byte(major, len(items)))
        for key, value in items.items():
            self.encode(key)
            self.encode(value)

    def encode_bool(self, value: bool):
        major = 7
        "trueは21、falseは20に割り当てられている"
        self.buff.write(
            convert_byte.encode_byte(major, 21)
            if value
            else convert_byte.encode_byte(major, 20)
        )

    def encode_none(self):
        major = 7
        self.buff.write(convert_byte.encode_byte(major, 22))
