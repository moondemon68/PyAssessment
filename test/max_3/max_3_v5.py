def max_3_v5(a,b,c):
  arr = []
  arr.append(a)
  arr.append(b)
  arr.append(c)
  max = arr[0]
  for i in arr:
    if (i>max):
      max=i
  return max