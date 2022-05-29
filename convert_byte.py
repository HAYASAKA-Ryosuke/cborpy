import struct

def encode_byte(major: int, length: int):
    """
    length < 24: 引数を付加情報に加える
    24 <= length < 2**8: 引数 + 24を付加情報に加える
    2**8 <= length < 2**16: 引数 + 25を付加情報に加える
    2**16 <= length < 2**32: 引数 + 26を付加情報に加える
    2**32 <= length < 2**64: 引数 + 27を付加情報に加える
    """
    if length < 24:
        return struct.pack('>B', (major << 5) | length)
    elif length < 2**8:
        return struct.pack('>BB', (major << 5) | 24, length)
    elif length < 2**16:
        return struct.pack('>BH', (major << 5) | 25, length)
    elif length < 2**32:
        return struct.pack('>BI', (major << 5) | 26, length)
    elif length < 2**64:
        return struct.pack('>BQ', (major << 5) | 27, length)