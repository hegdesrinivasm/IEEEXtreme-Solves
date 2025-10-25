import sys
sys.setrecursionlimit(1 << 25)

def main():
    input_data = sys.stdin.buffer.read().split()
    if not input_data:
        return
    data_iterator = iter(input_data)
    num_nodes = int(next(data_iterator))

    adjacency_list = [[] for _ in range(num_nodes + 1)]
    for _ in range(num_nodes - 1):
        u = int(next(data_iterator)); v = int(next(data_iterator))
        adjacency_list[u].append(v)
        adjacency_list[v].append(u)

    parent_map = [0] * (num_nodes + 1)
    children_map = [[] for _ in range(num_nodes + 1)]
    traversal_order = []
    stack = [1]
    parent_map[1] = -1
    while stack:
        u = stack.pop()
        traversal_order.append(u)
        for neighbor in adjacency_list[u]:
            if neighbor == parent_map[u]:
                continue
            parent_map[neighbor] = u
            children_map[u].append(neighbor)
            stack.append(neighbor)

    signature_to_id = {}
    next_available_id = 0

    def get_id(signature_tuple):
        nonlocal next_available_id
        canonical_id = signature_to_id.get(signature_tuple)
        if canonical_id is None:
            canonical_id = next_available_id
            signature_to_id[signature_tuple] = canonical_id
            next_available_id += 1
        return canonical_id

    subtree_id = [0] * (num_nodes + 1)
    for u in reversed(traversal_order):
        if not children_map[u]:
            signature = ()
        else:
            child_ids_list = [subtree_id[child_node] for child_node in children_map[u]]
            child_ids_list.sort()
            signature = tuple(child_ids_list)
        subtree_id[u] = get_id(signature)

    up_branch_id = [None] * (num_nodes + 1)
    up_branch_id[1] = None  # root has no parent branch

    for u in traversal_order:
        num_children = len(children_map[u])
        child_ids = [subtree_id[child_node] for child_node in children_map[u]]

        sorted_child_ids = sorted(child_ids)
        import bisect

        base_signature_ids = sorted_child_ids.copy()
        if up_branch_id[u] is not None:
            bisect.insort(base_signature_ids, up_branch_id[u])

        full_signature = tuple(base_signature_ids)
        if u == 1:
            distinct_full_signature_ids = set()
        full_signature_id = get_id(full_signature)
        distinct_full_signature_ids.add(full_signature_id)

        for child_node in children_map[u]:
            canonical_id = subtree_id[child_node]
            position = bisect.bisect_left(base_signature_ids, canonical_id)
            up_signature_ids = []
            up_signature_ids.extend(base_signature_ids[:position])
            up_signature_ids.extend(base_signature_ids[position+1:])
            up_branch_id[child_node] = get_id(tuple(up_signature_ids))

    print(len(distinct_full_signature_ids))

if __name__ == "__main__":
    main()
