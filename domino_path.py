def build_chain(tiles, mask, endpoint, cache):
    if mask == 0:
        return True
    
    cache_key = (mask, endpoint)
    if cache_key in cache:
        return cache[cache_key]
    
    tile_count = len(tiles)
    for pos in range(tile_count):
        if not (mask & (1 << pos)):
            continue
        
        val1, val2 = tiles[pos]
        updated_mask = mask ^ (1 << pos)
        
        if endpoint == -1:
            if build_chain(tiles, updated_mask, val2, cache):
                cache[cache_key] = True
                return True
            if val1 != val2 and build_chain(tiles, updated_mask, val1, cache):
                cache[cache_key] = True
                return True
        else:
            if val1 == endpoint and build_chain(tiles, updated_mask, val2, cache):
                cache[cache_key] = True
                return True
            if val2 == endpoint and build_chain(tiles, updated_mask, val1, cache):
                cache[cache_key] = True
                return True
    
    cache[cache_key] = False
    return False

def solve_problem(pieces):
    piece_count = len(pieces)
    result = 0
    cache = {}
    
    for subset_mask in range(1, 1 << piece_count):
        popcount = bin(subset_mask).count('1')
        if popcount == 1:
            result += 1
        elif build_chain(pieces, subset_mask, -1, cache):
            result += 1
    
    return result

iterations = int(input())
for _ in range(iterations):
    tile_count = int(input())
    collection = []
    for _ in range(tile_count):
        value_a, value_b = map(int, input().split())
        collection.append((value_a, value_b))
    
    answer = solve_problem(collection)
    print(answer)
