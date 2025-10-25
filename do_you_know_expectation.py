import sys
from decimal import Decimal, getcontext, ROUND_HALF_UP
data = sys.stdin.read().strip().split()
if not data:
    sys.exit(0)
it = iter(data)
gn = int(next(it))
kappa = int(next(it))
seq = [int(next(it)) for _ in range(gn)]
qubit = []
for val in seq:
    x = val
    for b in qubit:
        if (x ^ b) < x:
            x ^= b
    if x:
        qubit.append(x)
qubit.sort(reverse=True)
r = len(qubit)
tot = 0
for m in range(1 << r):
    s = 0
    mm = m
    idx = 0
    while mm:
        if mm & 1:
            s ^= qubit[idx]
        idx += 1
        mm >>= 1
    tot += pow(s, kappa)
den = 1 << r
getcontext().prec = 60
res = Decimal(tot) / Decimal(den)
print(res.quantize(Decimal('1.00'), rounding=ROUND_HALF_UP))