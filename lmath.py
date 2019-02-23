import math


def ShiftLeft(a: int or float, n: int) -> int:
    if n >= 0:
        return int(a) << n
    else:
        return ShiftRight(a, -n)


def ShiftRight(a: int or float, n: int) -> int:
    if n >= 0:
        return abs(int(a) >> n)
    else:
        return ShiftLeft(a, -n)


def FloatToInteger(floatnum: float) -> (int or float, bool):
    if 0.0 == math.modf(floatnum)[0]:
        return int(floatnum), True
    else:
        return floatnum, False


def IntToFb(x: int) -> int:
    e = 0
    if x < 8:
        return x
    while x >= (8 << 4):
        x = (x + 0xf) >> 4
        e += 4

    while x >= (8 << 1):
        x = (x + 1) >> 1
        e += 1

    return ((e + 1) << 3) | (x - 8)


def FbToInt(x: int) -> int:
    if x < 8:
        return x
    else:
        return ((x & 7) + 8) << abs((x >> 3) - 1)
