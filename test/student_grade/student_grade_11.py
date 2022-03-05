# correct conditions, wrong return value
def student_grade_11(a):
    if a < 0:
        return "INVALIDA"
    elif a > 100:
        return "INVALIDA"
    elif 80 <= a and a <= 100:
        return "AA"
    elif 73 <= a and a <= 79:
        return "ABA"
    elif 65 <= a and a <= 72:
        return "BA"
    elif 57 <= a and a <= 64:
        return "BCA"
    elif 50 <= a and a <= 56:
        return "CA"
    elif 35 <= a and a <= 49:
        return "DA"
    else:
        return "EA"