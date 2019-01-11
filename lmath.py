import math


def ShiftLeft(a, n):
    if n >= 0:
        return int(a) << n
    else:
        return ShiftRight(a, -n)


def ShiftRight(a, n):
    if n >= 0:
        return abs(int(a) >> n)
    else:
        return ShiftLeft(a, -n)


def FloatToInteger(floatnum):
    if 0.0 == math.modf(floatnum)[0]:
        return int(floatnum), True
    else:
        return floatnum, False
