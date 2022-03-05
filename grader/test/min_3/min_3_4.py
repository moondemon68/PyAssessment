def min_3_4(a, b, c):
    if a < b and b < c:
        return a
    elif b < a and a < c:
        return b
    else:
        return c