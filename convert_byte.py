

def encode_byte(major: int, length: int):
    if length < 24:
        return int.to_bytes((major << 5) | length, 1, 'big')
    elif length < 2**8:
        return int.to_bytes((major << 5) + 24, 1, 'big') + int.to_bytes(length, 1, 'big')
    elif length < 2**16:
        return int.to_bytes((major << 5) + 25, 1, 'big') + int.to_bytes(length, 2, 'big')
    elif length < 2**32:
        return int.to_bytes((major << 5) + 26, 1, 'big') + int.to_bytes(length, 4, 'big')
    elif length < 2**64:
        return int.to_bytes((major << 5) + 27, 1, 'big') + int.to_bytes(length, 6, 'big')
