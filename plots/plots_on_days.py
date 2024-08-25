"""
Script to generate plots based on commit data for weekdays and weekends.

Usage:
    python plots_on_days.py <filename.csv> <plot_type>

Arguments:
    <filename.csv>: CSV file containing commit data.
    <plot_type>: String representing the requested plot type. Options are "freq_for_weekends" or any other string for total commits per period.

Returns:
    Depending on the chosen plot type, either a plot showing the frequency of commits for each weekend day across different time periods, 
    or a plot showing the total commits per period.

Dependencies:
    - numpy
    - matplotlib
    - csv

Example:
    python plots_on_days.py commit_data.csv freq_for_weekends
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import matplotlib.ticker as mticker
import sys

# Fetching the filename and plot_type from command line arguments
filename = sys.argv[1]
plot = sys.argv[2]

# List to store the number of commits for each day of the week in every time period
day = [[] for _ in range(7)]

sum_period = []

# Open the csv file and read its contents into the lists
with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    periods = next(reader)  # Skip header row

    # Copy the reader
    reader_copy1, reader_copy2 = tee(reader)
    num_of_periods = len(periods)
    period = [[] for _ in range(num_of_periods)]

    # Append the number of commits for each day in each period
    for row in reader_copy2:
        for i in range(1, len(period)):
            period[i].append(float(row[i]))
    
    # Append for each week day the number of commits for every period
    for i in range(len(period[1])):
        for j in range(1, len(period)):
            day[i].append(period[j][i])
    
    # Calculate total commits for each period
    for i in range(1, len(period)):
        sum_period.append(sum(period[i]))
    
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

rects = []

def freq_for_weekends():
    """
    Function to plot the frequency of commits for each weekend day across the different time periods.
    """
    x = np.arange(len(periods))
    width = 0.45
    offset = width * 1.5

    fig, ax = plt.subplots()

    for i in range(2):
        x_shift = x + (i - 1 / 2) * width
        rect = ax.bar(x_shift, day[i+5], width, label=days[i+5])
        rects.append(rect)

    ax.set_ylabel('Frequencies', fontsize=35)
    ax.set_xlabel('Periods', fontsize=35)
    ax.set_xticks(x)
    ax.set_xticklabels(periods)
    ax.legend()

    # Set xtick labels with empty strings for every other label
    labels = ["" if i % 2 == 1 else periods[i] for i in range(len(periods))]
    ax.set_xticklabels(labels, rotation=45)
    
    # Set tick font size
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(35)

    # Format y-axis to show values in thousands
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'{int(x/1000)}'))


def total_commits_per_period():
    """
    Function to plot the total commits per period.
    """
    x = np.arange(len(periods))
    width = 0.45

    fig, ax = plt.subplots()
    rects.append(ax.bar(x, sum_period, width))

    ax.set_ylabel('Total Commits (Thousands)', fontsize=35)
    ax.set_xlabel('Period', fontsize=35)
    ax.set_xticks(x)

    # Set xtick labels with empty strings for every other label
    labels = ["" if i % 2 == 1 else periods[i] for i in range(len(periods))]
    ax.set_xticklabels(labels, rotation=45)
    
    # Set tick font size
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(35)

    # Format y-axis to show values in thousands
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'{int(x/1000)}'))


if plot == "freq_for_weekends":
    periods = periods[1:]
    freq_for_weekends()
else:
    periods = periods[1:]
    total_commits_per_period()

plt.show()