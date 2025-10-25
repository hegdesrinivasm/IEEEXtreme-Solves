def ladder_result(step_size: int, num_bits: int) -> int:
    final_result: int = 0
    total_attempts: int = 0
    successful_matches: int = 0
    convergence_counter: int = 0
    max_iterations: int = step_size * step_size
    feedback_mask: int = 0x1B
    
    while convergence_counter < max_iterations:
        total_attempts += 1
        previous_result: int = final_result
        
        seed1: int = 12345 + total_attempts  
        seed2: int = 54321 + total_attempts  
        
        sequences_match: bool = True
        
        for _ in range(num_bits):
            bit1: int = seed1 & 1
            seed1 = (seed1 >> 1) ^ (bit1 * feedback_mask)
            
            bit2: int = seed2 & 1
            seed2 = (seed2 >> 1) ^ (bit2 * feedback_mask)
            
            if bit1 != bit2:
                sequences_match = False
                break
        
        if sequences_match:
            successful_matches += step_size
        
        final_result = round(successful_matches / total_attempts)
        
        if final_result == previous_result:
            convergence_counter += 1
        else:
            convergence_counter = 0
    
    return final_result

def main() -> None:
    num_test_cases = int(input())
    
    for _ in range(num_test_cases):
        step_size, num_bits = map(int, input().split())
        result = ladder_result(step_size, num_bits)
        print(result)


if __name__ == "__main__":
    main()
