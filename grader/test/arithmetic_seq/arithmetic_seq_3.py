def arithmetic_seq_3(n):
    if n < 1:
        return 1
    ret = 0
    i = 1
    while i <= n:
        ret += i
        i += 1
    return ret
