def fib(x):
	dp = [0 for _ in range(1005)]
	dp[0] = 1
	dp[1] = 1
	for i in range(2, x + 1):
		dp[i] = dp[i - 1] + dp[i - 2]
	return dp[x]
