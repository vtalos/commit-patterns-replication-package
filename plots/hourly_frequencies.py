#!/usr/bin/env python3
"""
Script to generate a grouped bar chart showing the frequency of commits for each 
block of hour within two specific time periods.

Usage: 
    python hourly_frequencies.py <filename.csv> <period_name1> <period_name2>

Arguments:
    <filename.csv>: CSV file containing commit data.
    <period_name1>: String representing the name of the first time period.
    <period_name2>: String representing the name of the second time period.

Returns:
    A grouped bar chart showing the frequency of commits for each hour within 
    the specified time periods.

Dependencies:
    - numpy
    - matplotlib
    - csv

Example:
    python hourly_frequencies.py ../write-data-in-csv/csv-files/CommitPercentagesPerHour.csv 2015 2024
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib.ticker as mticker

def read_csv_data(filename):
    """
    Read CSV data and return headers and data dictionary.
    
    Parameters:
    filename (str): Path to the CSV file
    
    Returns:
    tuple: (headers, data_dict) where headers is a list of column names
           and data_dict maps column names to lists of values
    """
    data_dict = {}
    headers = []
    
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        
        # Initialize data dictionary
        for header in headers:
            data_dict[header] = []
        
        # Read data
        for row in reader:
            for header in headers:
                if header == 'Hour':
                    data_dict[header].append(row[header])
                else:
                    data_dict[header].append(float(row[header]))
    
    return headers, data_dict

def extract_period_data(data_dict, period1, period2):
    """
    Extract data for two specific periods.
    
    Parameters:
    data_dict (dict): Dictionary containing all data
    period1 (str): Name of first period
    period2 (str): Name of second period
    
    Returns:
    tuple: (hours, period1_data, period2_data)
    """
    if period1 not in data_dict:
        raise ValueError(f"Period '{period1}' not found in data")
    if period2 not in data_dict:
        raise ValueError(f"Period '{period2}' not found in data")
    
    hours = data_dict['Hour']
    period1_data = data_dict[period1]
    period2_data = data_dict[period2]
    
    return hours, period1_data, period2_data

def format_hour_labels(hours):
    """
    Format hour labels for better readability.
    
    Parameters:
    hours (list): List of hour strings
    
    Returns:
    list: Formatted hour labels
    """
    formatted = []
    for hour in hours:
        # Convert "HH:00" to "HH"
        if ':' in hour:
            formatted.append(hour.split(':')[0])
        else:
            formatted.append(hour)
    return formatted

def create_grouped_bar_chart(hours, period1_data, period2_data, period1_name, period2_name):
    """
    Create a professional grouped bar chart suitable for academic papers.
    
    Parameters:
    hours (list): Hour labels
    period1_data (list): Data for first period
    period2_data (list): Data for second period
    period1_name (str): Name of first period
    period2_name (str): Name of second period
    """
    # Set up the figure with academic styling
    fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
    
    # Format data
    x = np.arange(len(hours))
    width = 0.35
    
    # Academic-appropriate colors (colorblind-friendly and print-safe)
    # Using a deep blue and a warm orange - standard academic palette
    colors = ['#1f77b4', '#ff7f0e']  # Blue and orange from matplotlib's default cycle
    
    # Create bars with academic colors
    bars1 = ax.bar(x - width/2, period1_data, width, 
                   label=period1_name, color=colors[0],
                   edgecolor='white', linewidth=0.5)
    bars2 = ax.bar(x + width/2, period2_data, width,
                   label=period2_name, color=colors[1],
                   edgecolor='white', linewidth=0.5)
    
    # Customize axes with academic styling
    ax.set_xlabel('Hour', fontsize=12, fontname='DejaVu Serif')
    ax.set_ylabel('Commits (%)', fontsize=12, fontname='DejaVu Serif')
    
    # Format x-axis
    formatted_hours = format_hour_labels(hours)
    ax.set_xticks(x)
    ax.set_xticklabels(formatted_hours, fontsize=10, fontname='DejaVu Serif')
    
    # Format y-axis
    ax.tick_params(axis='y', labelsize=10)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    
    # Professional grid
    ax.yaxis.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    
    # Clean up spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Professional legend
    legend = ax.legend(fontsize=11, loc='upper left', frameon=True, 
                      facecolor='white', framealpha=1, edgecolor='gray')
    
    # Set font for legend text
    for text in legend.get_texts():
        text.set_fontname('DejaVu Serif')
    
    # Set tick parameters for academic style
    for label in ax.get_xticklabels():
        label.set_fontname('DejaVu Serif')
    for label in ax.get_yticklabels():
        label.set_fontname('DejaVu Serif')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    output_filename = f'percentages_per_hour_{period1_name}vs{period2_name}.pdf'
    plt.savefig(output_filename, format='pdf', bbox_inches='tight', pad_inches=0.1)
    
    print(f"Chart saved as: {output_filename}")
    
    # Show the plot
    plt.show()

def main():
    """
    Main function to execute the script workflow.
    """
    if len(sys.argv) != 4:
        print("Usage: python hourly_frequencies.py <filename.csv> <period_name1> <period_name2>")
        print("Example: python hourly_frequencies.py data.csv 2015 2024")
        sys.exit(1)
    
    filename = sys.argv[1]
    period1_name = sys.argv[2]
    period2_name = sys.argv[3]
    
    try:
        # Read data
        headers, data_dict = read_csv_data(filename)
        print(f"Successfully read data from {filename}")
        print(f"Available periods: {[h for h in headers if h != 'Hour']}")
        
        # Extract period data
        hours, period1_data, period2_data = extract_period_data(data_dict, period1_name, period2_name)
        
        # Create the chart
        create_grouped_bar_chart(hours, period1_data, period2_data, period1_name, period2_name)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()