"""
Script to generate a grouped bar chart showing the frequency of commits for each block of hour within two specific time periods.

Usage:
    python hourly_frequencies <filename.csv> <period_name1> <period_name2>

Arguments:
    <filename.csv>: CSV file containing commit data.
    <period_name1>: String representing the name of the first time period.
    <period_name2>: String representing the name of the second time period.

Returns:
    A grouped bar chart showing the frequency of commits for each hour within the specified time periods.

Dependencies:
    - numpy
    - matplotlib
    - csv

Example:
    python hourly_frequencies CommitPercentagesPerHour.csv 2004 2023
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
from itertools import tee

def read_csv(filename):
    """
    Function to read the CSV file and return the hours and period data.

    Parameters:
        filename (str): The name of the CSV file.

    Returns:
        hours (list): List of hour blocks.
        periods (list): List of period names.
        period_data (list of lists): List containing commit frequencies for each period.
    """
    hours = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        periods = next(reader)  # Skip header row
        
        reader_copy1, reader_copy2, reader_copy3 = tee(reader, 3)
        period_data = [[] for _ in range(len(periods))]

        for row in reader_copy2:
            for i in range(1, len(period_data)):
                period_data[i].append(float(row[i]))

        for row in reader_copy3:
            hours.append(row[0])

    return hours, periods, period_data

def hourly_frequencies(hours, period_hours1, period_hours2, period_name1, period_name2):
    """
    Function to plot the frequency of commits for each hour within two specific time periods.

    Parameters:
        hours (list): List of hour blocks.
        period_hours1 (list): Commit frequencies for the first period.
        period_hours2 (list): Commit frequencies for the second period.
        period_name1 (str): Name of the first period.
        period_name2 (str): Name of the second period.
    """
    x = np.arange(len(hours))
    width = 0.35  # Width of the bars

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - width/2, period_hours1, width, label=period_name1)
    rects2 = ax.bar(x + width/2, period_hours2, width, label=period_name2)

    ax.set_ylabel('Commits (%)', fontsize=35)
    ax.set_xlabel('Hour', fontsize=35)
    ax.set_xticks(x)
    ax.set_xticklabels(hours, rotation=45)

    ax.legend(fontsize=30)

    # Set tick font size
    labels = ["" if i % 2 == 1 else hours[i] for i in range(len(hours))]
    ax.set_xticklabels(labels)

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(35)

    fig.tight_layout()

    plt.show()

def main():
    """
    Main function to execute the script.
    """
    if len(sys.argv) != 4:
        print("Usage: python hourly_frequencies <filename.csv> <period_name1> <period_name2>")
        sys.exit(1)

    filename = sys.argv[1]
    period_name1 = sys.argv[2]
    period_name2 = sys.argv[3]

    hours, periods, period_data = read_csv(filename)

    # Identify the indices of the periods
    try:
        period_index1 = periods.index(period_name1)
        period_index2 = periods.index(period_name2)
    except ValueError:
        print(f"Error: One or both periods '{period_name1}' and '{period_name2}' not found in the data.")
        sys.exit(1)

    # Plot the hourly frequencies for the two periods
    hourly_frequencies(hours, period_data[period_index1], period_data[period_index2], period_name1, period_name2)

if __name__ == "__main__":
    main()