"""
Script to calculate and plot the ratio of commits inside and outside the 9 - 5 shift over the years.

Usage:
    python commits_inside_to_outside_common_shift_ratio.py <filename.csv>

Arguments:
    <filename.csv>: CSV file containing commit data for each year (columns) with timestamps (rows).

Returns:
    A plot showing the ratio of commits inside and outside the 9 - 5 shift over the years.

Dependencies:
    - matplotlib
    - numpy
    - pandas

Example:
    python commits_inside_to_outside_common_shift_ratio.py commits_data.csv
"""

import matplotlib.pyplot as plt
import sys
import numpy as np
import pandas as pd

# The csv file name to gather the data
filename = sys.argv[1]

# Reading data from the CSV file
data=pd.read_csv(filename)
data = data.iloc[:,1:]
data = np.array(data)

# Calculating average commits during 9 to 5 shift
commits_in_9_to_5 = data.T[:,9:17]
avg_commits_in_9_to_5_shift= np.sum(commits_in_9_to_5, axis=1) / 8

# Calculating average commits outside 9 to 5 shift
commits_outside_9_to_5 = data.T[:, np.r_[0:8, 17:24]]
avg_commits_outside_9_to_5_shift = np.sum(commits_outside_9_to_5, axis=1) /16

# Plotting
fig, ax = plt.subplots()

ax.set_xlabel('Year', fontsize=35)
ax.set_ylabel('Ratio', fontsize=35)
ax.set_xticks(range(2004,2024,2))
ax.set_xticklabels(range(2004,2024,2), rotation=45)
ax.plot(range(2004, 2024), avg_commits_in_9_to_5_shift / avg_commits_outside_9_to_5_shift, 
        linestyle='-', marker='o', color='blue', linewidth=5, markersize=15)

# Set tick font size
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(30)

# Set tick font size
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(30)

plt.grid(True)
plt.show()