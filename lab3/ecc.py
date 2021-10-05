import sys


# works
def read_input():
    xy = [int(x) for x in sys.stdin.readline().rstrip().replace('(', '').replace(')', '').replace(',', '').split()]
    abp = [int(x) for x in sys.stdin.readline().rstrip().split()]
    mn = [int(x) for x in sys.stdin.readline().rstrip().split()]
    return xy[0], xy[1], abp[0], abp[1], abp[2], mn[0], mn[1]


def multiply_points(original_x, original_y, x, y, n, a, p):
    if n == 1:
        return x, y
    else:
        new_x, new_y = add_points(original_x, x, original_y, y, a, p)
        return multiply_points(original_x, original_y, new_x, new_y, n - 1, a, p)


# works
def add_points(x1, x2, y1, y2, a, p):
    m = calculate_m(x1, x2, y1, y2, a, p)
    new_x = ((m ** 2) - x1 - x2) % p
    new_y = (m * (x1 - new_x) - y1) % p

    return new_x, new_y


# works
def modular_inverse(m, n):
    for x in range(1, n):
        if ((m % n) * (x % n)) % n == 1:
            return x
    return -1


# works
def calculate_m(x1, x2, y1, y2, a, p):
    if x1 == x2 and y1 == y2:
        m = ((3 * (x1 ** 2) + a) * modular_inverse(2 * y1, p)) % p
    else:
        m = ((y2 - y1) * modular_inverse((x2 - x1), p)) % p
    return m


def main():
    x, y, a, b, p, m, n = read_input()
    temp_x, temp_y = multiply_points(x, y, x, y, m, a, p)
    new_x, new_y = multiply_points(temp_x, temp_y, temp_x, temp_y, n, a, p)

    print('(' + str(new_x) + ', ' + str(new_y) + ')')


if __name__ == '__main__':
    main()
