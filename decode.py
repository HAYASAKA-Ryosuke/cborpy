
def decode(value: str):
    decoder = Decoder()
    result = decoder.decode(bytes.fromhex(value))
    return result

class Decoder:

    def __init__(self):
        self.index = 0

    def get_major(self, value: bytes):
        return value[0] >> 5

    def _length(self, values: bytes):
        if values[0] & 0x1F < 24:
            length = values[0] & 0x1F
        if values[0] & 0x1F == 24:
            length = values[0:1] & 0x1F
        if values[0] & 0x1F == 25:
            length = values[0:2] & 0x1F
        if values[0] & 0x1F == 26:
            length = values[0:3] & 0x1F
        if values[0] & 0x1F == 27:
            length = values[0:4] & 0x1F
        return length

    def _pad(self, values: bytes):
        if values[0] & 0x1F < 24:
            pad = 0
        if values[0] & 0x1F == 24:
            pad = 1
        if values[0] & 0x1F == 25:
            pad = 2
        if values[0] & 0x1F == 26:
            pad = 4
        if values[0] & 0x1F == 27:
            pad = 8
        return pad

    def decode(self, value):
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

    def decode_int(self, value: bytes, is_negative: bool=False):
        pad = self._pad(value)
        if pad > 0:
            result = int.from_bytes(value[1:pad+1], 'big')
            self.index += pad + 1
        else:
            result = value[0] & 0x1F
            self.index += 1

        if is_negative:
            return -(result + 1)

        return result
    
    def decode_byte(self, value: bytes):
        length = self._length(value)
        self.index += length + 1
        return  value[1:length + 1]

    def decode_str(self, value: bytes):
        length = self._length(value)
        if value[0] & 0x1F < 24:
            self.index += length + 1
            return value[1:length+1].decode()
        if value[0] & 0x1F == 24:
            self.index += length + 2
            return value[2:length+2].decode()
        if value[0] & 0x1F == 25:
            self.index += length + 3
            return value[3:length+3].decode()
        if value[0] & 0x1F == 26:
            self.index += length + 4
            return value[4:length+4].decode()
        if value[0] & 0x1F == 27:
            self.index += length + 5
            return value[5:length+5].decode()

    def decode_list(self, values: bytes):
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
        self.index += 1
        for i in range(length):
            result.append(self.decode(values[pad + self.index:]))
        self.index += length
        return result

    def decode_dict(self, values: bytes):
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
        result = {}
        index = 0
        key = ''
        list_bytes = values
        self.index += 1
        for i in range(length):
            key =  self.decode(list_bytes[pad + self.index:])
            value = self.decode(list_bytes[pad + self.index:])
            result[key] = value
        self.index += length
        return result