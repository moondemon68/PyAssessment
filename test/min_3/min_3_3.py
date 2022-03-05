def min_3_3(a, b, c):
    if a <= b:
        if a <= c:
            return a
        else:
            return c
    else:
        if b <= c:
            return b
        else:
            return c