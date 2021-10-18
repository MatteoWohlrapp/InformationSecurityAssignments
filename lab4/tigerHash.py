import sys
from sbox import *
from operation import *

UNIT = 64
BIT = 8


def read_input():
    return sys.stdin.buffer.read()


def pad(text):
    padded_text = text + b'\x01'
    while len(padded_text) % UNIT != 56:
        padded_text += b'\x00'
    return padded_text + (len(text)).to_bytes(8, 'big')


# w is 8 byte (64 bit)
# w[i] is 1 byte (8 bit)
def key_schedule(w):
    w[0] = and4(w[0] - and4(w[7] ^ 0xA5A5A5A5A5A5A5A5))
    # w[0] = minus(w[0], xor(w[7], bt(0xA5A5A5A5A5A5A5A5)))
    # w[1] = xor(w[1], w[0])
    w[1] = and4(w[1] ^ w[0])
    # w[2] = plus(w[2], w[1])
    w[2] = and4(w[2] + w[1])
    # w[3] = minus(w[3], xor(w[2], (~w[1]) << 19))
    w[3] = and4(w[3] - and4(w[2] ^ and4(~w[1] << 19)))
    w[4] = and4(w[4] ^ w[3])
    w[5] = and4(w[5] + w[4])
    w[6] = and4(w[6] - and4(w[5] ^ and4(~w[4]) >> 23))
    w[7] = and4(w[7] ^ w[6])
    w[0] = and4(w[0] + w[7])
    w[1] = and4(w[1] - and4(w[0] ^ and4(~w[7]) << 19))
    w[2] = and4(w[2] ^ w[1])
    w[3] = and4(w[3] + w[2])
    w[4] = and4(w[4] - and4(w[3] ^ and4(~w[2]) >> 23))
    w[5] = and4(w[5] ^ w[4])
    w[6] = and4(w[6] + w[5])
    w[7] = and4(w[7] - and4(w[6] ^ 0x0123456789ABCDEF))
    return w


# a, b, c, w are 8 byte
def inner_round(a, b, c, w, m):
    c ^= w
    c &= 0xffffffffffffffff
    a -= s0[and3(c >> (0 * BIT))] ^ s1[and3(c >> (2 * BIT))] ^ s2[and3(c >> (4 * BIT))] ^ s3[and3(c >> (6 * BIT))]
    b += s3[and3(c >> (1 * BIT))] ^ s2[and3(c >> (3 * BIT))] ^ s1[and3(c >> (5 * BIT))] ^ s0[and3(c >> (7 * BIT))]
    b *= m
    a &= 0xffffffffffffffff
    b &= 0xffffffffffffffff
    c &= 0xffffffffffffffff
    # c = xor(c, w)
    # a = minus(a, xor(xor(xor(bt(s0[c[0]]), bt(s1[c[2]])), bt(s2[c[4]])), bt(s3[c[6]])))
    # b = plus(b, xor(xor(xor(bt(s3[c[1]]), bt(s2[c[3]])), bt(s1[c[5]])), bt(s0[c[7]])))
    # b = multi(b, m)
    return a, b, c


def inner_rounds(a, b, c, W, m):
    a, b, c = inner_round(a, b, c, W[0], m)
    a, b, c = inner_round(b, c, a, W[1], m)
    a, b, c = inner_round(b, c, a, W[2], m)
    a, b, c = inner_round(b, c, a, W[3], m)
    a, b, c = inner_round(b, c, a, W[4], m)
    a, b, c = inner_round(b, c, a, W[5], m)
    a, b, c = inner_round(b, c, a, W[6], m)
    a, b, c = inner_round(b, c, a, W[7], m)
    return c, a, b


def outer_rounds(W, a, b, c):
    # a, b, c = 0x0123456789ABCDEF, 0xFEDCBA9876543210, 0xF096A5B4C3B2E187
    aa, bb, cc = a, b, c
    F = 0xFFFFFFFFFFFFFFFF
    # F5
    a, b, c = inner_rounds(a, b, c, W, 5)
    # F7
    W = key_schedule(W)
    a, b, c = inner_rounds(a, b, c, W, 7)
    # F9
    W = key_schedule(W)
    a, b, c = inner_rounds(a, b, c, W, 9)
    # Finally
    a ^= aa
    b = (b - bb) & F
    c = (c + cc) & F
    return a, b, c


def tiger_hash(X):
    a, b, c = 0x0123456789ABCDEF, 0xFEDCBA9876543210, 0xF096A5B4C3B2E187
    for x in X:
        W = [int.from_bytes(x[i:i + 8], 'big') for i in range(0, len(x), 8)]
        print(W)
        a, b, c = outer_rounds(W, a, b, c)
    return a, b, c


def main():
    text = read_input()
    padded_text = pad(text)
    X = [padded_text[i:i + UNIT] for i in range(0, len(padded_text), UNIT)]  # each 512 bits (64 bytes)
    a,b,c = tiger_hash(X)
    hash = a.to_bytes(8, 'big') + b.to_bytes(8, 'big') + c.to_bytes(8, 'big')
    print(hash)
    sys.stdout.buffer.write(hash)


if __name__ == '__main__':
    main()
