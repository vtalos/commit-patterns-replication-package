"""
Script to plot the number of contributors from results.txt for each year.

Usage:
    contributors_plot.py <filename.txt>

Arguments:
    <filename.txt>: txt file containing the number of contributors for each year for all of the sample,
    in this case the results.txt file.

Returns:
    A plot showing the number of contributors for the sample for each year.

Dependencies:
    - matplotlib
    - sys
Example:
    python contributors_plot.py results.txt
"""

import matplotlib.pyplot as plt
import sys

filename = sys.argv[1]
years= []
contributors_per_year= []
#open the .txt and read its contents 
with open(filename, 'r') as file:
    lines = file.readlines()
    for line in lines:
        #for each line retrieve the year and the contributors
        year, _, contributors = line.strip().partition(':')
        years.append(int(year.strip()))
        contributors_per_year.append(int(contributors.strip()))
#set font sizes, ticks and plot the data
fig, ax = plt.subplots()
plt.plot(years, contributors_per_year, linestyle='-', marker='o', color='blue', linewidth=5, markersize=15)
ax.set_xlabel('Year', fontsize = 35)
ax.set_ylabel('Number of Contributors', fontsize = 35)
plt.xticks(range(2004, 2024, 2), rotation = 45)
plt.yticks(range(4000, 9000, 1000))
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(35)
plt.grid(True)
plt.show()

        