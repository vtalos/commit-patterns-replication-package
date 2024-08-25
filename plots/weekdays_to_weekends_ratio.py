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

# Plotting
fig, ax = plt.subplots()
ax.set_xlabel('Year', fontsize=35)
ax.set_ylabel('Ratio', fontsize=35)
ax.set_xticks(range(2004, 2024, 2))
ax.set_xticklabels(range(2004, 2024, 2), rotation=45)
ax.plot(years, ratio, linestyle='-', marker='o', color='blue', linewidth=5, markersize=15)

# Set tick font size
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontsize(35)

plt.grid(True)
plt.show()