def deret_false(n):
    summ=0
    for i in range (1,n+1,2):
        if summ > 10:
            return -1
        summ=summ + i
        i=0+i
    return summ