import sys


class FastScanner:
    """A very small fast scanner around sys.stdin.buffer.read().split().

    Usage:
      fs = FastScanner()
      a = fs.next_int()
      s = fs.next_str()
      while fs.has_next(): ...

    This is bytes-based under the hood and decodes strings lazily.
    """

    def __init__(self):
        self._data = sys.stdin.buffer.read().split()
        self._n = len(self._data)
        self._i = 0

    def has_next(self):
        return self._i < self._n

    def next_bytes(self):
        if not self.has_next():
            raise StopIteration
        v = self._data[self._i]
        self._i += 1
        return v

    def next_int(self):
        return int(self.next_bytes())

    def next_str(self):
        return self.next_bytes().decode()


def solve():
    """Default example solve() function.

    This template provides a safe, fast scanner and a minimal example:
    - If the input is empty, it exits quietly.
    - If the first integer is followed by more tokens, it's interpreted
      as number of test cases `t` and for each test-case we expect:
        n a1 a2 ... an
      The example prints the sum of the n numbers for each test-case.
    - Otherwise the single integer is printed.

    Replace the body of `solve()` with problem-specific logic.
    """

    fs = FastScanner()
    if not fs.has_next():
        return

    first = fs.next_int()

    # Heuristic: if there are tokens left after reading `first`, treat
    # `first` as number of testcases `t` and process that many cases.
    if fs.has_next():
        t = first
        for _ in range(t):
            if not fs.has_next():
                break
            # Example case format: n followed by n integers; print their sum
            n = fs.next_int()
            arr = [fs.next_int() for _ in range(n)]
            print(sum(arr))
    else:
        # Only a single integer in input — echo it
        print(first)


def main():
    solve()


if __name__ == "__main__":
    main()
