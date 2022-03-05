def student_grade_3(a):
    if a < 0:
        return "INVALID"
    elif a > 100:
        return "INVALID"
    elif 79 <= a and a <= 100:
        return "A"
    elif 72 <= a and a <= 79:
        return "AB"
    elif 64 <= a and a <= 72:
        return "B"
    elif 56 <= a and a <= 64:
        return "BC"
    elif 49 <= a and a <= 56:
        return "C"
    elif 35 <= a and a <= 49:
        return "D"
    else:
        return "E"