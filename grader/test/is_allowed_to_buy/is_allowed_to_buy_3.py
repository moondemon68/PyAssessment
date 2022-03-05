def is_allowed_to_buy_3(soap, mask, sanitizer, face_shield):
    if soap < 0 or mask < 0 or sanitizer < 0:
        return False
    elif soap > 3:
        return False
    elif (soap > 0 and sanitizer > 2) or sanitizer > 3:
        return False
    elif mask > 4 or (face_shield > 0 and mask > 2):
        return False
    elif face_shield > 4 or (face_shield > 2 and mask > 0):
        return False
    else:
        return True