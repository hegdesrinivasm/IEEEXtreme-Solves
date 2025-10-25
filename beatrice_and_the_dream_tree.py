import sys
sys.setrecursionlimit(1 << 25)

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))

    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(next(it)); v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    parent = [0] * (n + 1)
    children = [[] for _ in range(n + 1)]
    order = []
    stack = [1]
    parent[1] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if w == parent[u]:
                continue
            parent[w] = u
            children[u].append(w)
            stack.append(w)

    sig_to_id = {}
    next_id = 0

    def get_id(sig_tuple):
        nonlocal next_id
        cid = sig_to_id.get(sig_tuple)
        if cid is None:
            cid = next_id
            sig_to_id[sig_tuple] = cid
            next_id += 1
        return cid

    sub_id = [0] * (n + 1)
    for u in reversed(order):
        if not children[u]:
            sig = ()
        else:
            child_ids = [sub_id[ch] for ch in children[u]]
            child_ids.sort()
            sig = tuple(child_ids)
        sub_id[u] = get_id(sig)

    up_id = [None] * (n + 1)
    up_id[1] = None  # root has no parent branch

    for u in order:
        k = len(children[u])
        ch_ids = [sub_id[ch] for ch in children[u]]

        sorted_ids = sorted(ch_ids)
        import bisect

        base_ids = sorted_ids.copy()
        if up_id[u] is not None:
            bisect.insort(base_ids, up_id[u])

        full_sig = tuple(base_ids)
        if u == 1:
            distinct_full_ids = set()
        full_id = get_id(full_sig)
        distinct_full_ids.add(full_id)

        for ch in children[u]:
            cid = sub_id[ch]
            pos = bisect.bisect_left(base_ids, cid)
            up_list = []
            up_list.extend(base_ids[:pos])
            up_list.extend(base_ids[pos+1:])
            up_id[ch] = get_id(tuple(up_list))

    print(len(distinct_full_ids))

if __name__ == "__main__":
    main()
