import sys

PRIVATE_KEY_INVALID = -1
PUBLIC_KEY_INVALID = 0
VALID = 1


def gcd(x, y):
    if y == 0:
        return x
    return gcd(y, x % y)


def read_input():
    nums = sys.stdin.readline().rstrip()
    private_key = sys.stdin.readline().rstrip()
    public_key = sys.stdin.readline().rstrip()
    return nums, private_key, public_key


def parse_input(data):
    data = data.split()
    return [int(x) for x in data]


def summing_list(private_key):
    sums = [private_key[0]]
    for i in range(1, len(private_key)):
        sum = sums[i - 1] + private_key[i]
        sums.append(sum)
    return sums


def validate_private_key(nums, private_key):
    m, n = nums
    # GCD must be 1
    if gcd(m, n) != 1:
        return False
    sums = summing_list(private_key)
    # n must be bigger than the sum of super increasing knapsack
    if n <= sums[-1]:
        return False
    # knapsack must be super increasing
    for i in range(len(sums) - 1):
        if sums[i] >= private_key[i + 1]:
            return False
    return True


def validation(nums, private_key, public_key):
    m, n = nums
    if not validate_private_key(nums, private_key):
        return PRIVATE_KEY_INVALID
    if len(private_key) != len(public_key):
        return PUBLIC_KEY_INVALID
    for public, private in zip(public_key, private_key):
        if public != private * m % n:
            return PUBLIC_KEY_INVALID
    return VALID


def main():
    nums, private_key, public_key = read_input()
    nums = parse_input(nums)
    private_key = parse_input(private_key)
    public_key = parse_input(public_key)
    print(validation(nums, private_key, public_key))


if __name__ == '__main__':
    main()