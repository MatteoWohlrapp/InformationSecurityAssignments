import sys
import math
from collections import Counter

ALPHA_LEN = 26
A_LOW = ord('a')
E_SHIFT = 4


def read_range():
    left = sys.stdin.readline().strip()
    right = sys.stdin.readline().strip()

    return int(left), int(right)


def read_text():
    text = ''
    for line in sys.stdin:
        text += line

    text = ''.join(filter(str.isalpha, text)).lower()
    return text


def assign_bins(key_len, text):
    freq_vectors = []
    for i in range(key_len):
        ith_bin = text[i::key_len]
        freq_vectors.append(Counter(ith_bin))
    return freq_vectors


def standard_deviation(vector):
    values = vector.values()
    return math.sqrt(sum([x * x for x in values]) / ALPHA_LEN - (sum(values) / ALPHA_LEN) ** 2)


def find_best_freq_vectors(left, right, text):
    (best_SD, best_freq_vectors) = (-1, None)
    for key_len in range(left, right + 1):
        freq_vectors = assign_bins(key_len, text)
        new_SD = sum(map(standard_deviation, freq_vectors))
        if best_SD < new_SD:
            best_SD, best_freq_vectors = new_SD, freq_vectors

        print('The sum of {} std. devs: {:.2f}'.format(key_len, new_SD))

    return best_freq_vectors


def get_most_frequent_letters(freq_vectors):
    return [max(vector, key=vector.get) for vector in freq_vectors]


def shift(letters):
    key = ''
    for letter in letters:
        key += chr((ord(letter) - A_LOW - E_SHIFT) % ALPHA_LEN + A_LOW)
    return key


def break_vigenere(left, right, text):
    freq_vectors = find_best_freq_vectors(left, right, text)
    letters = get_most_frequent_letters(freq_vectors)
    key = shift(letters)
    print('\nKey guess:')
    print(key)


def main():
    left, right = read_range()
    text = read_text()
    break_vigenere(left, right, text)


if __name__ == '__main__':
    main()
