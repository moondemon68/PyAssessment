def no_of_triangle_9(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return 0
    elif a+b>c and a+c>b and b+c>a:
        return 3
    elif (a+b>c and a+c>b):
        return 2
    elif a+b>c or a+c>b or b+c>a:
        return 1
    else:
        return 0