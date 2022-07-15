def fib_inf(x):
	if x == 0:
		return 1
	elif x == 1:
		return 1
	else:
		return fib_inf(x) + fib_inf(x-1)
