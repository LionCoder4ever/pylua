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
