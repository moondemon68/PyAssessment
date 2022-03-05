def segiempat_11(n):
    ret = ''
    c1 = '*'
    c2 = '#'
    if (n==2):
        ret = c1+c1+'\n'+c1+c1
    elif (n>2):
        for i in range(n):
            ret += c1
        ret += '\n'
        j = 0
        while j < n-2:
            ret += c1
            for k in range(n-2):
                ret += c2
            ret += c1
            ret += '\n'
            j += 1
        for i in range(n):
            ret += c1
    return ret