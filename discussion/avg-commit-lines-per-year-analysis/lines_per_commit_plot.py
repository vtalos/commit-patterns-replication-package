"""
Script to plot the evolution of average number of inserted lines per commit
for each year for our sample.

Usage:
    python lines_per_commit_plot.py <filename.txt>

Arguments:
    <filename.txt>: txt file containing the average of inserted line per commits
    for each year for all of the sample, in this case the lines_per_commit.txt file.

Returns:
    A plot showing the ratio of commits per line for the sample for each year.

Dependencies:
    - matplotlib
    - sys
Example:
    python lines_per_commit_plot.py lines_per_commit.txt
"""
import matplotlib.pyplot as plt
import sys

filename = sys.argv[1]
years= []
lines_to_commits_ratio_per_year = []

# Open the .txt and read its contents 
with open(filename, 'r') as file:
    lines = file.readlines()
    for line in lines:
        # For each line retrieve the year and the contributors
        year, _, lines_to_commits_ratio = line.strip().partition(':')
        years.append(int(year.strip()))
        lines_to_commits_ratio_per_year.append(float(lines_to_commits_ratio.strip()))

print(years)
print(lines_to_commits_ratio_per_year)

# Set font sizes, ticks and plot the data
fig, ax = plt.subplots()

plt.plot(years, lines_to_commits_ratio_per_year, linestyle='-', marker='o', color='blue', linewidth=3, markersize=8)
ax.set_xlabel('Year', fontsize = 9)
ax.set_ylabel('Lines to Commits Ratio', fontsize = 9)
plt.xticks(range(2004, 2024, 2), rotation = 45)

for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(9)

plt.grid(True)
plt.savefig(f'inserted_lines_per_commit.pdf', format='pdf', bbox_inches='tight', pad_inches=0)     