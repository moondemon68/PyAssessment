def max_3_v2(a, b, c):
  if (a >= b) and (a >= c):
    return a
  elif (b >= a) and (b >= c):
    return b
  else:
    return c