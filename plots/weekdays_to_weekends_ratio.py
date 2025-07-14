"""
Script to calculate and plot the ratio of average weekday commits to average weekend day commits over the years.

Usage:
    python weekdays_to_weekends_ratio.py <filename.csv>

Arguments:
    <filename.csv>: CSV file containing commit data.

Returns:
    A plot showing the ratio of average weekday commits to average weekend day commits over the years.

Dependencies:
    - matplotlib
    - numpy
    - pandas

Example:
    python weekdays_to_weekends_ratio.py commit_data.csv
"""
import matplotlib.pyplot as plt
import sys
import numpy as np
import pandas as pd

# Fetching the filename from command line arguments
filename = sys.argv[1]

# Reading data from the CSV file
data = pd.read_csv(filename)

# Filter out the weekdays and weekends
weekdays = data.iloc[0:5, 1:].T
weekends = data.iloc[5:, 1:].T

# Calculate the average number of commits for weekdays and weekends
avg_n_of_commits_weekdays = np.mean(weekdays, axis=1)
avg_n_of_commits_weekends = np.mean(weekends, axis=1)

# Calculate the ratio of average weekday commits to average weekend commits
ratio = avg_n_of_commits_weekdays / avg_n_of_commits_weekends

# Extract the years from the column names
years = data.columns[1:].astype(int)

# Plotting with enhanced style
fig, ax = plt.subplots(figsize=(6, 4), dpi=300)

# Plot the ratio
ax.plot(
    years,
    ratio,
    linestyle='-',
    marker='o',
    color='#1f77b4',
    linewidth=3,
    markersize=6,
    label='Weekday to Weekend Commit Ratio'
)

# Axis Labels
ax.set_xlabel('Year', fontsize=12, fontname='DejaVu Serif')
ax.set_ylabel('Ratio', fontsize=12, fontname='DejaVu Serif')

# Ticks and Labels
ax.set_xticks(years)
ax.set_xticklabels(years, rotation=45, fontsize=10)
ax.tick_params(axis='y', labelsize=10)

# Optional: Add light grid
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Remove top/right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Tight layout to avoid label cut-off
plt.tight_layout()

# Save with high resolution
plt.savefig('weekdays_to_weekends_ratio.pdf', format='pdf', bbox_inches='tight')
