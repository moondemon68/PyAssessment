def digits_1(n):
    if n <= 10:
        return 1
    else:
        return 1 + digits_1(n/10)