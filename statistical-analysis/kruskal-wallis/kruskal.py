import pandas as pd
from scipy.stats import kruskal
import argparse
import sys
from scipy.stats import mannwhitneyu
from itertools import combinations

# Avoid UnicodeEncodeError on Windows
import os
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Perform Kruskal-Wallis test and then Mann-Whitney with correction factor")
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

alpha = 0.05

stat, p = kruskal(*groups)
print(f"Kruskal-Wallis: H = {stat:.3f}, p = {p:.4f}")

if p < 0.05:
    pairs = list(combinations(range(n), 2))
    alpha_adj = alpha / len(pairs)
    print("\nPost-hoc pairwise (Mann-Whitney U):") 
    print(f"Number of groups (n) = {n}")
    print(f"Total pairwise comparisons = {len(pairs)}")
    print(f"Using Bonferroni-adjusted alpha = {alpha_adj:.5f}\n")

    for i, j in pairs:
        stat_mw, p_mw = mannwhitneyu(groups[i], groups[j], alternative='two-sided')
        print(f"{day_labels[i]} vs {day_labels[j]}: p = {p_mw:.4f} | Significant: {p_mw < alpha_adj}")
else:
    print("There is not statistical significant (post-hoc tests not needed).")