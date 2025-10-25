def solve_visit_egypt():
    piastre_values = [25, 50, 100, 500, 1000, 2000, 5000, 10000, 20000]
    
    modulo_value = 10**9 + 7
    
    test_count = int(input())
    
    for _ in range(test_count):
        euros, mikel_guess, andrew_guess = map(int, input().split())
        
        total_piastres = euros * 53 * 100
        
        pathway_counts = [0] * (total_piastres + 1)
        pathway_counts[0] = 1
        
        for coin_value in piastre_values:
            for amount in range(coin_value, total_piastres + 1):
                pathway_counts[amount] = (pathway_counts[amount] + pathway_counts[amount - coin_value]) % modulo_value
        
        actual_modulo = pathway_counts[total_piastres]
        
        mikel_distance = abs(actual_modulo - mikel_guess)
        andrew_distance = abs(actual_modulo - andrew_guess)
        
        if mikel_distance < andrew_distance:
            print("Mikel")
        elif andrew_distance < mikel_distance:
            print("Andrew")
        elif mikel_guess == actual_modulo and andrew_guess == actual_modulo:
            print("TIE")
        else:
            print("NONE")


solve_visit_egypt()
