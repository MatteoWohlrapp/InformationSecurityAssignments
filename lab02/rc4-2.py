import sys


STREAM_LEN = 256


def parse_inputs(inputs):
    idx = inputs.find(b'\xff')
    key = inputs[:idx]
    data = inputs[idx+1:]
    return key, data


def initialize(key):
    S = [i for i in range(STREAM_LEN)]
    j = 0
    key_len = len(key)
    for i in range(STREAM_LEN):
        j = (j + S[i] + key[i % key_len]) % STREAM_LEN
        S[i], S[j] = S[j], S[i]
    return S


def make_keystream(S, data_len):
    K = []
    i, j = 0, 0
    for idx in range(STREAM_LEN + data_len):
        i = (i + 1) % STREAM_LEN
        j = (j + S[i]) % STREAM_LEN
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % STREAM_LEN
        K.append(S[t])
    return K


def xor(x, y):
    return bytes(a ^ b for a, b in zip(x, y))


def encrypt(key, data):
    S = initialize(key)
    keystream = make_keystream(S, len(data))
    keystream = keystream[STREAM_LEN:]
    ciphertext = xor(data, keystream)
    return ciphertext


def main():
    inputs = sys.stdin.buffer.read()
    key, data = parse_inputs(inputs)
    result = encrypt(key, data)
    sys.stdout.buffer.write(result)


if __name__ == '__main__':
    main()