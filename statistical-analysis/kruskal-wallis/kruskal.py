import pandas as pd
from scipy.stats import kruskal
import argparse
import sys

# Avoid UnicodeEncodeError on Windows
import os
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Perform Kruskal-Wallis test with Bonferroni correction.")
parser.add_argument("filename", help="Path to the CSV file")
args = parser.parse_args()

# Read CSV file
df = pd.read_csv(args.filename)

# Extract day labels and data
day_labels = df['Day'].tolist()
data = df.iloc[:, 1:].to_numpy()

# Prepare groups (list of lists)
groups = [list(row) for row in data]

# Number of groups (days)
n = len(groups)

# Total pairwise comparisons: nC2
total_comparisons = n * (n - 1) // 2
alpha = 0.05
alpha_adj = alpha / total_comparisons  # Bonferroni correction

print(f"Number of groups (n) = {n}")
print(f"Total pairwise comparisons = {total_comparisons}")
print(f"Using Bonferroni-adjusted alpha = {alpha_adj:.5f}\n")

# Perform pairwise Kruskal-Wallis tests
for i in range(n):
    for j in range(i + 1, n):
        stat, p_value = kruskal(groups[i], groups[j])
        print(f"Comparing {day_labels[i]} vs. {day_labels[j]}:")
        print(f"  H statistic = {stat:.4f}")
        print(f"  raw p-value = {p_value:.6f}")
        if p_value < alpha_adj:
            print(f"  --> Reject H₀ at α_adj={alpha_adj:.5f}: significant difference.\n")
        else:
            print(f"  --> Fail to reject H₀ at α_adj={alpha_adj:.5f}: no significant difference.\n")