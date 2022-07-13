def max_3_13(a, b, c):
    def test(d):
        return d + 3
    a = test(a)
    if a > b and a > c:
        return a
    elif b > a and b > c:
        return b
    else:
        return c
