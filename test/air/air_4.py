def air_4(t):
    if t <= 0:
	    return "PADAT"
    elif t > 0 and t < 100:
        return "CAIR"
    elif t > 100:
        return "GAS"
    else:
        return "ANTARA CAIR-GAS"