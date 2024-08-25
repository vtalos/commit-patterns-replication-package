"""
This script reads a CSV file containing time series data for various periods and 
plots a 100% stacked bar chart to visualize the distribution of data across specified 
time blocks. The user is prompted to input multiple time blocks (start and end) 
which are then used to aggregate the data accordingly.

Usage:
    python hourly_stacked_bar_chart.py <filename>
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys
import statsmodels.api as sm

def block_to_time(block, is_end=False):
    """
    Convert a block index to a time string in HH:00 format. 
    For end blocks, it returns time in HH:59 format.

    Parameters:
    block (int): The block index to convert.
    is_end (bool): Whether the block is an end block.

    Returns:
    str: The corresponding time in "HH:00" or "HH:59" format.
    """
    hours = block % 24
    if is_end:
        hours -= 1
        return f"{hours:02d}:59"
    else:
        return f"{hours:02d}:00"

def input_time_blocks():
    """
    Prompt the user to input multiple time blocks and return them as a list of tuples.

    Returns:
    list of tuples: A list where each tuple contains a start and end block index.
    """
    blocks = []
    while True:
        time_block_start = int(input("Enter the start time block (or type '-1' to stop): "))
        if time_block_start == -1:
            break
        time_block_end = int(input(f"Enter the end time block for start block {time_block_start}: "))
        blocks.append((time_block_start, time_block_end))
    return blocks

def read_data(filename):
    """
    Read data from the CSV file and organize it into periods and hourly blocks.

    Parameters:
    filename (str): The name of the CSV file to read.

    Returns:
    tuple: A tuple containing periods, hours, and period data.
    """
    hours = []
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

    return periods, hours, period

def prepare_data(period, time_blocks):
    """
    Prepare data for each time block and generate time labels.

    Parameters:
    period (list of lists): The period data.
    time_blocks (list of tuples): List of start and end block indices.

    Returns:
    tuple: A tuple containing the data blocks and time labels.
    """
    data_blocks = []
    time_labels = []

    for time_block_start, time_block_end in time_blocks:
        data = []
        for per in period:
            if len(per) > 0:
                if time_block_start != time_block_end:
                    total = sum(per[time_block_start:time_block_end])
                else:
                    total = per[time_block_start]
                data.append(total)
        
        data_blocks.append(data)
        
        start_time = block_to_time(time_block_start)
        end_time = block_to_time(time_block_end, is_end=True)
        time_labels.append(f"{start_time} - {end_time}")

    return np.array(data_blocks), time_labels

def plot_data(data_blocks, time_labels, periods):
    """
    Plot a 100% stacked bar chart based on the data blocks and time labels.

    Parameters:
    data_blocks (numpy array): Array of data blocks.
    time_labels (list of str): List of time labels for the legend.
    periods (list of str): List of period labels.
    """
    data_blocks_normalized = data_blocks / data_blocks.sum(axis=0)

    fig, ax = plt.subplots()

    bottom = np.zeros(len(periods))
    colors = plt.cm.viridis(np.linspace(0, 1, len(time_labels)))

    for i, data_block in enumerate(data_blocks_normalized):
        ax.bar(range(len(periods)), data_block, bottom=bottom, color=colors[i], width=0.85, label=time_labels[i])
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

    ax.legend(fontsize=25, loc='center right', bbox_to_anchor=(1, 0.4), facecolor='white', framealpha=1)

    plt.show()

def main(filename):
    """
    Main function to execute the script workflow.

    Parameters:
    filename (str): The name of the CSV file to process.
    """
    time_blocks = input_time_blocks()
    periods, hours, period = read_data(filename)
    periods = periods[1:len(periods)]
    data_blocks, time_labels = prepare_data(period, time_blocks)
    plot_data(data_blocks, time_labels, periods)

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)