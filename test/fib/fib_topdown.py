dp = [0 for _ in range(1005)]

def fib_topdown(x):
	if x == 0:
		return 1
	elif x == 1:
		return 1
	elif dp[x] != 0:
		return dp[x]
	else:
		dp[x] = fib_topdown(x-1) + fib_topdown(x-2)
		return dp[x]