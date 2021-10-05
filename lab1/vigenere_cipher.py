import sys

ALPHA_LEN = 26
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def read_query():
    return sys.stdin.readline().split()


def read_text_e():
    text = ''
    for line in open('encryptionTest'):
        text += line
    return text


def read_text_d():
    text = ''
    for line in open('decryptionTest'):
        text += line
    return text


def read_text():
    text = ''
    for line in sys.stdin:
        text += line

    text = text.rstrip('\n')
    return text


def decrypt(ciphertext, key):
    adjusted_key = key_padding(ciphertext, key)
    plaintext = ''
    index = 0

    for char in ciphertext:
        if char.isalpha():
            lower_char = char.lower()
            ciphertext_char_index = ALPHABET.index(lower_char) + 1
            key_char_index = ALPHABET.index(adjusted_key[index]) + 1
            new_index = (ciphertext_char_index - (key_char_index - 1)) % ALPHA_LEN - 1
            index += 1
            if char.isupper():
                upper_char = ALPHABET[new_index].upper()
                plaintext += upper_char
            else:
                plaintext += ALPHABET[new_index]
        else:
            plaintext += char

    return plaintext


def encrypt(plaintext, key):
    adjusted_key = key_padding(plaintext, key)
    ciphertext = ''
    index = 0

    for char in plaintext:
        if char.isalpha():
            lower_char = char.lower()
            plaintext_char_index = ALPHABET.index(lower_char) + 1
            key_char_index = ALPHABET.index(adjusted_key[index]) + 1
            new_index = (plaintext_char_index + (key_char_index - 1)) % ALPHA_LEN - 1
            index += 1
            if char.isupper():
                upper_char = ALPHABET[new_index].upper()
                ciphertext += upper_char
            else:
                ciphertext += ALPHABET[new_index]
        else:
            ciphertext += char

    return ciphertext


def key_padding(text, key):
    number_of_chars = 0

    for char in text:
        if char.isalpha():
            number_of_chars += 1

    adjusted_key = ''
    key_length = len(key)

    for i in range(0, number_of_chars):
        adjusted_key += key[i % key_length]

    return adjusted_key


def main():
    query = read_query()
    mode = query[0]
    key = query[1]
    result = ''

    if mode == 'd':
        result = decrypt(read_text(), key)
    elif mode == 'e':
        result = encrypt(read_text(), key)
    print(result)


if __name__ == '__main__':
    main()
