def air_8(t):
    if t < 0:
	    return "PADAT"
    elif t > 0 and t < 100:
        return "CAIR"
    elif t > 100:
        return "GAS"
    elif t == 0:
        return "ANTARA PADAT-CAIR"
    else:
        return "ANTARA CAIR"