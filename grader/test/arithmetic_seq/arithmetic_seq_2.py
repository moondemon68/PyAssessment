def arithmetic_seq_2(n):
    if n < 1:
        return 1
    ret = 0
    for i in range(1, n+1):
        ret += i
    return ret
