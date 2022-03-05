def max_3_v4(a, b, c):
  if (a>=b):
    if (a>=c):
      return a
    else:
      return c
  else:
    if (b>=c):
      return b
    else:
      return c