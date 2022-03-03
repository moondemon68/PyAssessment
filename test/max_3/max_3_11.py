def max_3_11(a, b, c):
    c -= 1 * a + b
    if a > b and a > c:
        return a
    elif b > a and b > c:
        return b
    else:
        return c-1+a*2

