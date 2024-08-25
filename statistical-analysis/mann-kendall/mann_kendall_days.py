"""
This script performs the Mann-Kendall trend test on commit data from a CSV file, 
analyzing trends in the number of commits made on a specified day of the week over 
a series of time periods.

The script reads commit data from a CSV file where each row corresponds to a day of the week 
and each column (after the first) corresponds to a specific time period (e.g., years). 
It then applies the Mann-Kendall test to determine if there is a statistically significant 
trend in the number of commits over time for the specified day.

Finally, it generates a plot showing the number of commits over the time periods and 
highlights the trend if a significant one is detected.

Usage:
    python mann_kendall_days.py <filename> <day_of_week>

Arguments:
    filename: The path to the CSV file containing commit data.
    day_of_week: The day of the week to analyze (0=Monday, 6=Sunday).
"""


import pymannkendall as mk
import sys
import argparse
from itertools import tee
import csv
import matplotlib.pyplot as plt

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments containing filename and day.
    """
    parser = argparse.ArgumentParser(description="A script for implementing Mann-Kendall Test on weekly data.")
    parser.add_argument("filename", help="The CSV file to get the data from.")
    parser.add_argument("day", help="The day of the week to implement the Mann-Kendall Test (0=Monday, 6=Sunday).", type=int)
    return parser.parse_args()

def read_csv_data(filename):
    """
    Read data from a CSV file.

    Args:
        filename (str): The name of the CSV file.

    Returns:
        list: A list containing the period labels (years).
        list: A list of lists where each sublist contains commits for each weekday across periods.
        list: A list of the total number of commits for each period.
    """
    day_total = []
    all_commits = [[] for _ in range(7)]
    sum_period = []

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        periods = next(reader)  # Skip header row
        reader_copy1, reader_copy2 = tee(reader)
        num_of_periods = len(periods)
        period = [[] for _ in range(num_of_periods)]

        for row in reader_copy2:
            for i in range(1, len(period)):
                period[i].append(float(row[i]))

        for i in range(len(period[1])):
            total_commits = 0
            for j in range(1, len(period)):
                all_commits[i].append(period[j][i])
                total_commits += period[j][i]
            day_total.append(total_commits)

        for i in range(1, len(period)):
            sum_period.append(sum(period[i]))

    periods = periods[1:len(periods)]
    return periods, all_commits, sum_period

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
        periods (list): The period labels (years).
        data (list): The data to be plotted.
        p_value (float): The p-value from the Mann-Kendall test.
        alpha (float): The significance level. Default is 0.05.
    """
    fig, ax = plt.subplots()

    plt.xlabel('Year', fontsize=35)
    plt.ylabel('Commits (%)', fontsize=35)
    plt.grid(True)
    plt.xticks(rotation=40)

    labels = ["" if i % 2 == 1 else periods[i] for i in range(len(periods))]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45)

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(35)

    if p_value < alpha:
        plt.plot(periods, data, marker='o', linestyle='-', color='red', label='Trend Line', linewidth=5, markersize=15)
    else:
        plt.plot(periods, data, marker='o', linestyle='-', linewidth=5, markersize=15)

    plt.show()

def main():
    """
    Main function to execute the Mann-Kendall test script.
    """
    args = parse_arguments()

    periods, all_commits, sum_period = read_csv_data(args.filename)

    data = all_commits[args.day]

    test_statistic, p_value = perform_mann_kendall_test(data)

    interpretation = interpret_mann_kendall_result(test_statistic, p_value)
    print(interpretation)

    plot_data(periods, data, p_value)

if __name__ == "__main__":
    main()