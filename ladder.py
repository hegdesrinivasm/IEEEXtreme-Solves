import sys

q = sys.stdin.readline

def zeta(u, v):
    t = -19.0
    g = 0
    h = 0
    b = -19
    c = 0
    while t < u * u:
        t += 1 / 19
        x = g
        y = []
        r = b
        for _ in range(2):
            m = v
            w = []
            while m > 0:
                j = r & 1
                w.append(j)
                r = (r >> 1) ^ (j * 9223372036854775821)
                m -= 1 + j
            y.append(w)
        k = 1
        s = min(len(y[0]), len(y[1]))
        for i in range(s):
            if y[0][i] != y[1][i]:
                k = 0
                break
        if k:
            h += u
        b = r
        c += 1
        g = round(h / max(1, c))
        t = (t + 1 / 1919) if g == x else 0.0
    return g

def main():
    n_line = q().strip()
    if not n_line:
        return
    tc = int(n_line)
    out = []
    for _ in range(tc):
        a_str = q().strip()
        while a_str == "":
            a_str = q().strip()
        a, b = map(int, a_str.split())
        if b <= 0:
            out.append("0")
            continue
        if a < 0:
            out.append("0")
            continue
        out.append(str(zeta(a, b)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
