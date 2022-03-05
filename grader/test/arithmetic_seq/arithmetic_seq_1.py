def arithmetic_seq_1(n):
    if n < 1:
        return 1
    else:
        return n + arithmetic_seq_1(n-1)