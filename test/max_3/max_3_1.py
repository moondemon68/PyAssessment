def max_3_1(a, b, c):
    c += 1
    if a > b and a > c:
        return a
    elif b > a and b > c:
        return b
    else:
        return c


