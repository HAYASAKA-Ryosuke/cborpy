import struct


def decode(value: str):
    decoder = Decoder()
    result = decoder.decode(bytes.fromhex(value))
    return result


class Decoder:
    def __init__(self) -> None:
        self.index = 0

    def get_major(self, value: bytes) -> int:
        return value[0] >> 5

    def _length(self, values: bytes) -> int:
        if values[0] & 0x1F < 24:
            return int(values[0]) & 0x1F
        if values[0] & 0x1F == 24:
            return int(values[0:1]) & 0x1F
        if values[0] & 0x1F == 25:
            return int(values[0:2]) & 0x1F
        if values[0] & 0x1F == 26:
            return int(values[0:3]) & 0x1F
        if values[0] & 0x1F == 27:
            return int(values[0:4]) & 0x1F
        raise ValueError(f"Invalid value {values!r}")

    def _pad(self, values: bytes) -> int:
        if values[0] & 0x1F < 24:
            return 0
        if values[0] & 0x1F == 24:
            return 1
        if values[0] & 0x1F == 25:
            return 2
        if values[0] & 0x1F == 26:
            return 4
        if values[0] & 0x1F == 27:
            return 8
        raise Exception(f"Invalid value: {values!r}")

    def decode(self, value) -> int | bytes | str | list | dict | float:
        major = self.get_major(value)
        if major == 0:
            return self.decode_int(value)
        elif major == 1:
            return self.decode_int(value, True)
        elif major == 2:
            return self.decode_byte(value)
        elif major == 3:
            return self.decode_str(value)
        elif major == 4:
            return self.decode_list(value)
        elif major == 5:
            return self.decode_dict(value)
        elif major == 7:
            return self.decode_major7(value)
        raise Exception(f"Invalid value: {value}")

    def decode_int(self, value: bytes, is_negative: bool = False) -> int:
        pad = self._pad(value)
        if pad > 0:
            result = int.from_bytes(value[1 : pad + 1], "big")
            self.index += pad + 1
        else:
            result = value[0] & 0x1F
            self.index += 1

        if is_negative:
            return -(result + 1)

        return result

    def decode_byte(self, value: bytes) -> bytes:
        length = self._length(value)
        self.index += length + 1
        return value[1 : length + 1]

    def decode_str(self, value: bytes) -> str:
        length = self._length(value)
        if value[0] & 0x1F < 24:
            self.index += length + 1
            return value[1 : length + 1].decode()
        if value[0] & 0x1F == 24:
            self.index += length + 2
            return value[2 : length + 2].decode()
        if value[0] & 0x1F == 25:
            self.index += length + 3
            return value[3 : length + 3].decode()
        if value[0] & 0x1F == 26:
            self.index += length + 4
            return value[4 : length + 4].decode()
        if value[0] & 0x1F == 27:
            self.index += length + 5
            return value[5 : length + 5].decode()

        raise Exception(f"Invalid value: {value!r}")

    def decode_list(self, values: bytes) -> list:
        length = 0
        pad = 0
        if values[0] & 0x1F < 24:
            pad = 0
            length = int(values[0]) & 0x1F
        if values[0] & 0x1F == 24:
            pad = 1
            length = int(values[0:1]) & 0x1F
        if values[0] & 0x1F == 25:
            pad = 2
            length = int(values[0:2]) & 0x1F
        if values[0] & 0x1F == 26:
            pad = 3
            length = int(values[0:3]) & 0x1F
        if values[0] & 0x1F == 27:
            pad = 4
            length = int(values[0:4]) & 0x1F
        result = []
        self.index += 1
        for i in range(length):
            result.append(self.decode(values[pad + self.index :]))
        self.index += length
        return result

    def decode_dict(self, values: bytes) -> dict:
        length = 0
        pad = 0
        if values[0] & 0x1F < 24:
            pad = 0
            length = int(values[0]) & 0x1F
        if values[0] & 0x1F == 24:
            pad = 1
            length = int(values[0:1]) & 0x1F
        if values[0] & 0x1F == 25:
            pad = 2
            length = int(values[0:2]) & 0x1F
        if values[0] & 0x1F == 26:
            pad = 3
            length = int(values[0:3]) & 0x1F
        if values[0] & 0x1F == 27:
            pad = 4
            length = int(values[0:4]) & 0x1F
        result = {}
        self.index += 1
        for i in range(length):
            key = self.decode(values[pad + self.index :])
            value = self.decode(values[pad + self.index :])
            result[key] = value
        self.index += length
        return result

    def decode_major7(self, values: bytes) -> float | bool | None:
        if values == b'\xf5':
            return True
        elif values == b'\xf4':
            return False
        elif values == b'\xf6':
            return None
        else:
            return struct.unpack(">d", values[1:])[0]
