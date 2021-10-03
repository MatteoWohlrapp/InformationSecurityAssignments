import sys, io, os


BLOCK_SIZE = 8
HALF_SIZE = 4


# split data
def split_data(data):
    return [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]


# split keys
def split_key(key):
    return [key[i:i+HALF_SIZE] for i in range(0, len(key), HALF_SIZE)]


# xor function
def xor(x, y):
    return bytes(a ^ b for a, b in zip(x, y))


# encrypt fiestel
def encrypt(keys, blocks):
    cipher = bytearray()
    for block in blocks:
        L, R = block[:HALF_SIZE], block[HALF_SIZE:]
        for key in keys:
            L, R = R, xor(L, key)
        cipher += L + R
    return cipher


# decrypt fiestel
def decrypt(keys, blocks):
    plain = bytearray()
    for block in blocks:
        L, R = block[:HALF_SIZE], block[HALF_SIZE:]
        for key in keys:
            L, R = xor(R, key), L
        plain += L + R
    return plain


# perform fiestel cipher
def fiestel(method, keys, blocks):
    if method == b'\x65':
        return encrypt(keys, blocks)
    else:
        return decrypt(keys[::-1], blocks)


# parse inputs
def parse_inputs(inputs):
    method = inputs[0]
    rest = inputs[2:]
    idx = rest.find(b'\xff')
    key = rest[:idx]
    data = rest[idx+1:]
    return method, key, data


def main():
    inputs = sys.stdin.buffer.read()  # read input
    method, key, data = parse_inputs(inputs)  # parse input
    blocks = split_data(data)  # split data in to blocks of 8 bytes
    keys = split_key(key)  # split keys into blocks of 4 bytes
    sys.stdout.buffer.write(fiestel(method, keys, blocks))  # print result


if __name__ == '__main__':
    main()
