import sys


def read_bytes():
    return sys.stdin.buffer.read()


def split_input(bs):
    key = []
    data = []
    at_key = True

    for byte in bs:
        if at_key:
            if byte and 0xff == 0:
                at_key = False
            else:
                key += byte
        else:
            data += byte
    return [key, data]


def transform(key, data):
    cipher = []
    for i in range(0, len(key) - 1):
        cipher.append(bytes([a ^ b for a, b in zip(key[i], data[i])]))

    binary = ''
    for i in range(0, len(cipher) - 1):
        binary += bin(bytes(cipher[i]))

    return binary


def main():

    bs = read_bytes()
    data = split_input(bs)
    key = data[0]
    data = data[1]

    transformed_bytes = transform(key, data)

    print(transformed_bytes)


if __name__ == '__main__':
    main()
