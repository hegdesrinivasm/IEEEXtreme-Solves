piastre_values = [25, 50, 100, 500, 1000, 2000, 5000, 10000, 20000]
modulo_value = 10**9 + 7
total_piastres = 10 * 53 * 100

pathway_counts = [0] * (total_piastres + 1)
pathway_counts[0] = 1

for coin_value in piastre_values:
    for amount in range(coin_value, total_piastres + 1):
        pathway_counts[amount] = (pathway_counts[amount] + pathway_counts[amount - coin_value]) % modulo_value

print(f"Total piastres: {total_piastres}")
print(f"Answer: {pathway_counts[total_piastres]}")
print(f"Expected: 96479252")
print(f"Mikel guess: 10, distance: {abs(pathway_counts[total_piastres] - 10)}")
print(f"Andrew guess: 25, distance: {abs(pathway_counts[total_piastres] - 25)}")
