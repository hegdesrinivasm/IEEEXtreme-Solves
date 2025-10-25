def triplets(n):
    if (n & (n + 1)) == 0:
        return None
    
    num1, num2, num3 = 1, n, n - 1
    if num3 > 0 and num1 != num2 and num1 != num3 and num2 != num3:
        if (num1 ^ num2 ^ num3) == n:
            return (num1, num2, num3)
    
    if n >= 3:
        num1, num2, num3 = 2, n + 1, n - 3
        if num3 > 0 and num1 != num2 and num1 != num3 and num2 != num3:
            if num1 + num2 + num3 == 2 * n and (num1 ^ num2 ^ num3) == n:
                return (num1, num2, num3)
    
    return None

t = int(input())
for _ in range(t):
    n = int(input())
    result = solve(n)
    if result is None:
        print(-1)
    else:
        print(*result)