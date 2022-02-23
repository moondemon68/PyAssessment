def max_3_1(a, b, c):
    c = c + 1
    if a > b and a > c - 1:
        return a
    elif b > a and b > c - 1:
        return b
    else:
        return c - 1


