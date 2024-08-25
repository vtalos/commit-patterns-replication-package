"""
This script reads commit data from a CSV file, allows the user to select specific days of the week (Monday to Sunday), 
and generates a stacked bar chart showing the number or proportion of commits for each selected day over different periods (e.g., years). 
The script is designed to visualize how commit activity varies across the selected days over time.

Usage:
    python daily_stacked_bar_chart.py <filename>

Arguments:
    filename: The name of the CSV file containing the commit data. The CSV file should have periods (e.g., years) as headers 
              and rows corresponding to different time intervals.

The script will prompt the user to input the days of the week they want to analyze, where days are represented as integers 
(0=Monday, 6=Sunday). A stacked bar chart will then be displayed for the selected days.
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse
from itertools import tee

# Define the days of the week
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def input_days_of_week():
    """
    Prompt the user to input multiple days of the week and return them as a list of integers.

    Returns:
    list of int: A list where each integer corresponds to a day of the week (0=Monday, 6=Sunday).
    """
    days = []
    print("Enter the days of the week as integers (0=Monday, 6=Sunday).")
    while True:
        day = int(input("Enter a day (or type '-1' to stop): "))
        if day == -1:
            break
        elif 0 <= day <= 6:
            days.append(day)
        else:
            print("Invalid input. Please enter a value between 0 and 6.")
    return days

def read_data(filename):
    """
    Read data from the CSV file and organize it into periods and daily commits.

    Parameters:
    filename (str): The name of the CSV file to read.

    Returns:
    tuple: A tuple containing periods, hours, and period data.
    """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        periods = next(reader)  # Skip header row
        reader_copy1, reader_copy2 = tee(reader, 2)
        num_of_periods = len(periods)
        period = [[] for _ in range(num_of_periods)]
        all_commits = [[] for _ in range(7)]

        for row in reader_copy1:
            for i in range(1, len(period)):
                period[i].append(float(row[i]))

        for i in range(len(period[1])):
            for j in range(1, len(period)):
                all_commits[i % 7].append(period[j][i])

    return periods[1:], all_commits

def prepare_data(all_commits, selected_days):
    """
    Prepare data for the selected days of the week.

    Parameters:
    all_commits (list of lists): The daily commits data.
    selected_days (list of int): List of selected days of the week (0=Monday, 6=Sunday).

    Returns:
    tuple: A tuple containing the data for the selected days and their corresponding labels.
    """
    data_blocks = []
    day_labels = []

    for day in selected_days:
        data_blocks.append(all_commits[day])
        day_labels.append(days[day])  # Use the global 'days' list to get the day names

    return np.array(data_blocks), day_labels

def plot_data(data_blocks, day_labels, periods):
    """
    Plot a stacked bar chart based on the data blocks and day labels.

    Parameters:
    data_blocks (numpy array): Array of data blocks.
    day_labels (list of str): List of day labels for the legend.
    periods (list of str): List of period labels.
    """
    fig, ax = plt.subplots()

    bottom = np.zeros(len(periods))
    colors = plt.cm.viridis(np.linspace(0, 1, len(day_labels)))

    for i, data_block in enumerate(data_blocks):
        ax.bar(range(len(periods)), data_block, bottom=bottom, color=colors[i], width=0.85, label=day_labels[i])
        bottom += data_block

    plt.xlabel('Year', fontsize=35)
    plt.ylabel('Commits (%)', fontsize=35)

    labels = ["" if i % 2 == 1 else periods[i] for i in range(len(periods))]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45)

    plt.grid(True)
    plt.xticks(rotation=35)

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(35)

    ax.legend(fontsize=25, loc='upper right')

    plt.tight_layout()
    plt.show()

def main(filename):
    """
    Main function to execute the script workflow.

    Parameters:
    filename (str): The name of the CSV file to process.
    """
    selected_days = input_days_of_week()
    periods, all_commits = read_data(filename)
    data_blocks, day_labels = prepare_data(all_commits, selected_days)
    plot_data(data_blocks, day_labels, periods)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script for creating a stacked bar chart for selected days of the week.")
    parser.add_argument("filename", help="The CSV file to get the data from")
    args = parser.parse_args()
    main(args.filename)