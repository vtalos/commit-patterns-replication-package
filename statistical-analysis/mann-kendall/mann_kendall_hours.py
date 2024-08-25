"""
This script performs the Mann-Kendall trend test on time-blocked commit data from a CSV file, 
analyzing trends in the number of commits within a specified range of hours over a series of time periods.

The script reads commit data from a CSV file where each row corresponds to an hourly time block 
and each column (after the first) corresponds to a specific time period (e.g., years). 
It sums the number of commits across the specified range of time blocks and applies the Mann-Kendall 
test to determine if there is a statistically significant trend in the number of commits over time.

Finally, it generates a plot showing the number of commits over the time periods and 
highlights the trend if a significant one is detected.

Usage:
    python mann_kendall_hours.py <filename> <time_block_start> <time_block_end>

Arguments:
    filename: The path to the CSV file containing commit data.
    time_block_start: The starting hour block for analysis (0=00:00-01:00, 23=23:00-00:00).
    time_block_end: The ending hour block for analysis (inclusive).
"""
import pymannkendall as mk
import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys
import statsmodels.api as sm

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        tuple: A tuple containing the filename, start time block, and end time block.
    """
    if len(sys.argv) != 4:
        print("Usage: python mann_kendall_hours.py <filename> <time_block_start> <time_block_end>")
        sys.exit(1)

    filename = sys.argv[1]
    time_block_start = int(sys.argv[2])
    time_block_end = int(sys.argv[3])
    return filename, time_block_start, time_block_end

def read_csv_data(filename):
    """
    Read and process data from a CSV file.

    Args:
        filename (str): The path to the CSV file containing commit data.

    Returns:
        tuple: A tuple containing:
            - periods (list): The list of period labels (e.g., years).
            - hours (list): The list of hour blocks.
            - period_data (list of lists): Data where each sublist contains commits for each time block.
    """
    hours = []
    period_data = []

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        periods = next(reader)  # Skip header row
        reader_copy1, reader_copy2, reader_copy3 = tee(reader, 3)
        num_of_periods = len(periods)
        period = [[] for _ in range(num_of_periods)]

        for row in reader_copy2:
            for i in range(1, len(period)):
                period[i].append(float(row[i]))

        for row in reader_copy3:
            hours.append(row[0])

    return periods[1:], hours, period

def process_data(period, time_block_start, time_block_end):
    """
    Process commit data to compute totals for specified time blocks.

    Args:
        period (list of lists): Data where each sublist contains commits for each time block.
        time_block_start (int): The starting time block for analysis.
        time_block_end (int): The ending time block for analysis.

    Returns:
        list: A list of total commits for each period.
    """
    data = []

    for per in period:
        if len(per) > 0:
            if time_block_start != time_block_end:
                total = sum(per[time_block_start:time_block_end])
            else:
                total = per[time_block_start]
            data.append(total)

    return data

def perform_mann_kendall_test(data):
    """
    Perform the Mann-Kendall test on the provided data.

    Args:
        data (list): A list of commit counts to analyze.

    Returns:
        tuple: The Mann-Kendall test statistic and p-value.
    """
    result = mk.original_test(data)
    return result[0], result[2]

def interpret_mann_kendall_result(test_statistic, p_value, alpha=0.05):
    """
    Interpret the results of the Mann-Kendall test.

    Args:
        test_statistic (float): The Mann-Kendall test statistic.
        p_value (float): The p-value from the Mann-Kendall test.
        alpha (float): The significance level. Default is 0.05.

    Returns:
        str: Interpretation of the test results.
    """
    print("Mann-Kendall Test Statistic:", test_statistic)
    print("P-Value:", p_value)

    if p_value < alpha:
        return "There is a statistically significant trend in the data."
    else:
        return "There is no statistically significant trend in the data."

def plot_data(periods, data, p_value, alpha=0.05):
    """
    Plot the data with or without a trend line.

    Args:
        periods (list): The period labels (e.g., years).
        data (list): The data to be plotted.
        p_value (float): The p-value from the Mann-Kendall test.
        alpha (float): The significance level. Default is 0.05.
    """
    fig, ax = plt.subplots()

    plt.xlabel('Year', fontsize=35)
    plt.ylabel('Commits (%)', fontsize=35)

    # Set xtick labels with empty strings for every other label
    labels = ["" if i % 2 == 1 else periods[i] for i in range(len(periods))]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45)

    plt.grid(True)
    plt.xticks(rotation=35)

    # Set tick font size
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(35)

    # Display the trend line if exists
    if p_value < alpha:
        plt.plot(periods, data, marker='o', linestyle='-', color='red', label='Trend Line', linewidth=5, markersize=15)
    else:
        plt.plot(periods, data, marker='o', linestyle='-', linewidth=5, markersize=15)

    plt.show()

def main():
    """
    Main function to execute the script.
    """
    filename, time_block_start, time_block_end = parse_arguments()

    periods, hours, period_data = read_csv_data(filename)

    data = process_data(period_data, time_block_start, time_block_end)

    test_statistic, p_value = perform_mann_kendall_test(data)

    interpretation = interpret_mann_kendall_result(test_statistic, p_value)
    print(interpretation)

    plot_data(periods, data, p_value)

if __name__ == "__main__":
    main()