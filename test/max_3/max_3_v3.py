def max_3_v3(a, b, c):
  if (a>=b):
    if (a>=c):
      largest=a
    else:
      largest=c
  else:
    if (b>=c):
      largest=b
    else:
      largest=c
  return largest