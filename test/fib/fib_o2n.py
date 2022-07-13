def fib_o2n(x):
	if x == 0:
		return 1
	elif x == 1:
		return 1
	else:
		return fib_o2n(x-1) + fib_o2n(x-2)
