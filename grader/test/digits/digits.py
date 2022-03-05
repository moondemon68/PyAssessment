def digits(n):
    if n < 10:
        return 1
    else:
        return 1 + digits(n/10)