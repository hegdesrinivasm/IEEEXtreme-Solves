# filename: squared_gaps_alignment.py
import sys

def read_ints():
    return list(map(int, sys.stdin.readline().split()))

def main():
    input_data = sys.stdin.read().strip().split()
    if not input_data:
        return
    it = iter(input_data)
    len_a = int(next(it))
    string_a = next(it).strip()
    len_b = int(next(it))
    string_b = next(it).strip()
    match_score = int(next(it))
    mismatch_penalty = int(next(it))
    gap_penalty = int(next(it))

    # Use a large negative number for -infinity
    NEGATIVE_INFINITY = -10**18

    # We will iterate over rows i = 0..len_a and columns j = 0..len_b
    # Maintain rolling arrays for prev row (j=0..len_b): match_dp_prev, gap_a_dp_prev, gap_b_dp_prev
    # And compute current row arrays: match_dp_curr, gap_a_dp_curr, gap_b_dp_curr
    # For X (gaps in A, advancing j), we need current segment length per cell to compute extension.
    # For Y (gaps in B, advancing i), we need previous row's Y lengths and current cell's Y length.

    # Arrays size len_b+1
    match_dp_prev = [NEGATIVE_INFINITY] * (len_b + 1)
    gap_a_dp_prev = [NEGATIVE_INFINITY] * (len_b + 1)
    gap_b_dp_prev = [NEGATIVE_INFINITY] * (len_b + 1)

    # Track gap lengths for Y in previous row (i-1, j): gap_b_len_prev[j]
    gap_b_len_prev = [0] * (len_b + 1)
    # Track gap lengths for X in previous row: not needed; X extends along j horizontally within same row
    # For row i=0 initialization:
    match_dp_prev[0] = 0
    gap_a_dp_prev[0] = NEGATIVE_INFINITY
    gap_b_dp_prev[0] = NEGATIVE_INFINITY
    gap_b_len_prev[0] = 0

    # First row (i=0): we can only insert gaps in A to align b[1..len_b]
    # X at (0,j): one contiguous gap segment in A of length j with cost j^2 * gap_penalty
    # We can compute incrementally: cost increase from j-1 to j is (2*(j-1)+1) * gap_penalty
    # Also make sure starting at j=1 comes from match_dp_prev[0] (which is 0)
    # We also keep current X length along the row
    gap_a_len_row = 0
    for j in range(1, len_b + 1):
        if j == 1:
            # starting a new gap from state at (0,0)
            gap_start_base = max(match_dp_prev[0], gap_b_dp_prev[0])
            gap_a_dp_prev[j] = gap_start_base + gap_penalty  # 1^2 * gap_penalty
            gap_a_len_row = 1
        else:
            # extend the existing X segment
            gap_extend_increment = (2 * gap_a_len_row + 1) * gap_penalty
            gap_a_dp_prev[j] = gap_a_dp_prev[j - 1] + gap_extend_increment
            gap_a_len_row += 1
        match_dp_prev[j] = NEGATIVE_INFINITY  # cannot match/mismatch without i>0
        gap_b_dp_prev[j] = NEGATIVE_INFINITY  # cannot have Y gaps (they advance i)
        gap_b_len_prev[j] = 0

    # Now iterate rows i=1..len_a
    for i in range(1, len_a + 1):
        match_dp_curr = [NEGATIVE_INFINITY] * (len_b + 1)
        gap_a_dp_curr = [NEGATIVE_INFINITY] * (len_b + 1)
        gap_b_dp_curr = [NEGATIVE_INFINITY] * (len_b + 1)

        # Track lengths for X along current row, and Y lengths per cell
        # For X we track per j incrementally: gap_a_len_at_prev_j
        gap_a_len_at_prev_j = 0  # length of X at j-1 within this row (for extension)
        gap_b_len_curr = [0] * (len_b + 1)

        # j = 0 column: only Y gaps (advancing i) possible
        if i == 1:
            # start Y segment from (0,0)
            gap_start_base = max(match_dp_prev[0], gap_a_dp_prev[0])
            gap_b_dp_curr[0] = gap_start_base + gap_penalty
            gap_b_len_curr[0] = 1
        else:
            # extend Y from (i-1,0)
            prev_gap_len = gap_b_len_prev[0]
            gap_extend_increment = (2 * prev_gap_len + 1) * gap_penalty
            gap_b_dp_curr[0] = gap_b_dp_prev[0] + gap_extend_increment
            gap_b_len_curr[0] = prev_gap_len + 1

        # match_dp_curr[0] stays -inf, gap_a_dp_curr[0] stays -inf (cannot advance j at j=0 for X from same row without starting)
        match_dp_curr[0] = NEGATIVE_INFINITY
        gap_a_dp_curr[0] = NEGATIVE_INFINITY

        # Now j=1..len_b
        for j in range(1, len_b + 1):
            # Compute M[i][j]
            match_mismatch_score = match_score if string_a[i - 1] == string_b[j - 1] else mismatch_penalty
            match_dp_curr[j] = max(match_dp_prev[j - 1], gap_a_dp_prev[j - 1], gap_b_dp_prev[j - 1]) + match_mismatch_score

            # Compute X[i][j]: gaps in A, advancing j
            # Option 1: start new X segment after finishing at (i, j-1) with non-X state
            gap_a_start_base = max(match_dp_curr[j - 1], gap_b_dp_curr[j - 1])
            gap_a_start_cost = gap_a_start_base + gap_penalty  # length 1 segment
            # Option 2: extend existing X from (i, j-1)
            if gap_a_dp_curr[j - 1] != NEGATIVE_INFINITY:
                gap_extend_increment = (2 * gap_a_len_at_prev_j + 1) * gap_penalty
                gap_a_extend_cost = gap_a_dp_curr[j - 1] + gap_extend_increment
                optimal_gap_a_score = max(gap_a_start_cost, gap_a_extend_cost)
                if gap_a_extend_cost >= gap_a_start_cost:
                    gap_a_len_at_prev_j += 1
                else:
                    gap_a_len_at_prev_j = 1
            else:
                optimal_gap_a_score = gap_a_start_cost
                gap_a_len_at_prev_j = 1
            gap_a_dp_curr[j] = optimal_gap_a_score

            # Compute Y[i][j]: gaps in B, advancing i
            # Option 1: start new Y segment from max(match_dp_prev[j], gap_a_dp_prev[j]) at (i-1, j)
            gap_b_start_base = max(match_dp_prev[j], gap_a_dp_prev[j])
            gap_b_start_cost = gap_b_start_base + gap_penalty
            # Option 2: extend existing Y from (i-1, j)
            if gap_b_dp_prev[j] != NEGATIVE_INFINITY:
                prev_gap_len = gap_b_len_prev[j]
                gap_b_extend_increment = (2 * prev_gap_len + 1) * gap_penalty
                gap_b_extend_cost = gap_b_dp_prev[j] + gap_b_extend_increment
                if gap_b_extend_cost >= gap_b_start_cost:
                    gap_b_dp_curr[j] = gap_b_extend_cost
                    gap_b_len_curr[j] = prev_gap_len + 1
                else:
                    gap_b_dp_curr[j] = gap_b_start_cost
                    gap_b_len_curr[j] = 1
            else:
                gap_b_dp_curr[j] = gap_b_start_cost
                gap_b_len_curr[j] = 1

        # Roll rows
        match_dp_prev, gap_a_dp_prev, gap_b_dp_prev = match_dp_curr, gap_a_dp_curr, gap_b_dp_curr
        gap_b_len_prev = gap_b_len_curr

    final_score = max(match_dp_prev[len_b], gap_a_dp_prev[len_b], gap_b_dp_prev[len_b])
    print(final_score)

if __name__ == "__main__":
    main()
