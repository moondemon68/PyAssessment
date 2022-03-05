def pow3abs(a):
    res = a * a * a
    if res < 0:
        return res * -1
    return res