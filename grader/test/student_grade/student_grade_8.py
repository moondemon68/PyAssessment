def student_grade_8(a):
    if a < 0:
        return "INVALID"
    elif a > 100:
        return "INVALID"
    elif 80 <= a and a <= 100:
        return "A"
    elif 65 <= a and a <= 72:
        return "B"
    elif 50 <= a and a <= 56:
        return "C"
    elif 35 <= a and a <= 49:
        return "D"
    else:
        return "E"