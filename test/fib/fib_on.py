dp = [0 for _ in range(1005)]

def fib_on(x):
	if x == 0:
		return 1
	elif x == 1:
		return 1
	elif dp[x] != 0:
		return dp[x]
	else:
		dp[x] = fib_on(x-1) + fib_on(x-2)
		return dp[x]