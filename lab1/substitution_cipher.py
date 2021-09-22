import sys

A_UP = ord('A')
A_LOW = ord('a')
ALPHA_LEN = 26


def read_query():
    query_blocks = sys.stdin.readline().strip().split()
    queries = []
    for i in range(0, len(query_blocks)-1, 2):
        queries.append((query_blocks[i], query_blocks[i+1]))
    return queries


def read_text():
    text = ''
    for line in sys.stdin:
        text += line
    return text.rstrip()


def shift(text, val):
    string = ''
    shift_val = val % ALPHA_LEN
    # print(val, shift_val)
    for c in text:
        if c.isalpha():
            if c.lower():
                string += chr((ord(c) - A_LOW + shift_val) % ALPHA_LEN + A_LOW)
            else:
                string += chr((ord(c) - A_UP + shift_val) % ALPHA_LEN + A_UP)
        else:
            string += c
    return string


def map_enc(text, mapping):
    string = ''
    for c in text:
        if c.isalpha():
            if c.islower():
                string += mapping[ord(c) - A_LOW].lower()
            else:
                string += mapping[ord(c) - A_UP].upper()
        else:
            string += c

    return string


def map_dec(text, mapping):
    string = ''

    for c in text:
        if c.isalpha():
            if c.islower():
                string += chr(mapping.find(c) + A_LOW)
            else:
                string += chr(mapping.find(c) + A_UP)
        else:
            string += c

    return string


def apply_queries(queries, text):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    for (method, val) in queries:
        if val.isalpha():
            if method == 'e':
                alphabet = map_enc(alphabet, val)
            else:
                alphabet = map_dec(alphabet, val)
        else:
            if method == 'e':
                alphabet = shift(alphabet, int(val))
            else:
                alphabet = shift(alphabet, -int(val))

    return map_enc(text, alphabet)


def main():
    queries = read_query()
    text = read_text()

    result = apply_queries(queries, text)
    print(result)


if __name__ == '__main__':
    main()
