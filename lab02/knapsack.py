import sys


def read_input():
    public_key = sys.stdin.readline().rstrip()
    nums = ""
    for line in sys.stdin:
        nums = nums + line + " "
    return public_key, nums


def parse_input(data):
    data = data.split()
    return [int(x) for x in data]


def summing_list(private_key):
    sums = [private_key[0]]
    for i in range(1, len(private_key)):
        sum = sums[i - 1] + private_key[i]
        sums.append(sum)
    return sums


def encrypt(key, n):
    sum = 0
    i = 0
    while n > 0:
        if n % 2:
            sum += key[i]
        n //= 2
        i += 1
    return sum


def decrypt(SK, m, n, c):
    m = (n + 1) // m
    knapsack_sum = c * m % n
    x = 0
    for sk in SK:
        x *= 2
        if knapsack_sum >= sk:
            knapsack_sum -= sk
            x += 1
    return x


def main():
    type = sys.stdin.readline().rstrip()
    if type == "e":
        public_key, nums = read_input()
        public_key = parse_input(public_key)
        nums = parse_input(nums)
        for n in nums:
            print(encrypt(public_key, n))
    if type == "d":
        mn = parse_input(sys.stdin.readline().rstrip())
        SK, nums = read_input()
        m, n = mn[0], mn[1]
        SK = parse_input(SK)
        nums = parse_input(nums)
        SK.reverse()
        for c in nums:
            print(decrypt(SK, m, n, c))


if __name__ == '__main__':
    main()
