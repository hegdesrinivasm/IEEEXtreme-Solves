piastre_values = [25, 50, 100, 500, 1000, 2000, 5000, 10000, 20000]
modulo_value = 10**9 + 7

test_cases = [
    (10, 10, 25),
    (1, 443443317, 3000000),
    (40, 338770238, 338770238),
    (60, 338770238, 318903897),
    (100, 572914301, 572914315)
]

for euros, mikel_guess, andrew_guess in test_cases:
    total_piastres = euros * 53 * 100
    
    pathway_counts = [0] * (total_piastres + 1)
    pathway_counts[0] = 1
    
    for coin_value in piastre_values:
        for amount in range(coin_value, total_piastres + 1):
            pathway_counts[amount] += pathway_counts[amount - coin_value]
    
    actual_modulo = pathway_counts[total_piastres] % modulo_value
    
    print(f"Euros: {euros}, Actual: {actual_modulo}, Mikel: {mikel_guess}, Andrew: {andrew_guess}")
    print(f"Mikel distance: {abs(actual_modulo - mikel_guess)}, Andrew distance: {abs(actual_modulo - andrew_guess)}")
    print()
