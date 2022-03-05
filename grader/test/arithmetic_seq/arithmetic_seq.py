def arithmetic_seq(n):
    if n <= 1:
        return 1
    else:
        return n + arithmetic_seq(n-1)