def min_3_5(a, b, c):
    if a < b and b < c:
        return a
    elif b < c:
        return b
    else:
        return c