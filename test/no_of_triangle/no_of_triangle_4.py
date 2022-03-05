def no_of_triangle_4(a, b, c):
    if a+b>c and a+c>b and b+c>a:
        return 3
    elif (a+b>c and a+c>b) or (a+c>b and b+c>a):
        return 2
    elif a+b>c or a+c>b or b+c>a:
        return 1
    elif a <= 0 or b <= 0 or c <= 0:
        return 0
    else:
        return 0