mask = 0xFFFFFFFFFFFFFFFF.to_bytes(8, 'big')


def bt(x):
    return x.to_bytes(8, 'big')


def xor(x, y):
    return and2(bytes(and3(a ^ b) for a, b in zip(x, y)))


def minus(x, y):
    return and2(bytes(and3(a - b) for a, b in zip(x, y)))


def plus(x, y):
    return and2(bytes(and3(a + b) for a, b in zip(x, y)))


def multi(x, m):
    return and2(bytes(and3(a * m) for a in x))


def and_(x, y):
    return and2(bytes(and3(a & b) for a, b in zip(x, y)))


def and2(x):
    return bytes(a & b for a, b in zip(x, mask))


def and3(a):
    return a & 0XFF


def and4(a):
    return a & 0xFFFFFFFFFFFFFFFF
