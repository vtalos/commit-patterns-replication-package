"""
Script to generate a bar chart showing total commits per period.

Usage:
    python total_commits_per_period.py <filename.csv>

Arguments:
    <filename.csv>: CSV file containing commit data.

Returns:
    A bar chart showing the total commits per period.

Dependencies:
    - numpy
    - matplotlib
    - csv
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import sys

def read_data(filename):
    """
    Read data from CSV file and calculate total commits per period.
    
    Parameters:
    filename (str): Path to the CSV file
    
    Returns:
    tuple: (periods, total_commits_per_period)
    """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        periods = next(reader)[1:]  # Skip first column header
        
        period_data = [[] for _ in range(len(periods))]
        
        for row in reader:
            for i, value in enumerate(row[1:]):  # Skip first column
                period_data[i].append(float(value))
        
        # Calculate total commits for each period
        total_commits = [sum(period) for period in period_data]
    
    return periods, total_commits

def plot_total_commits(periods, total_commits):
    """
    Plot total commits per period.
    
    Parameters:
    periods (list): List of period names
    total_commits (list): List of total commits for each period
    """
    x = np.arange(len(periods))
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    # Professional color
    color = '#4C72B0'
    
    ax.bar(x, total_commits, width=0.6, color=color, 
           edgecolor='white', linewidth=1.0)
    
    ax.set_ylabel('Total Commits (Thousands)', fontsize=18, fontname='DejaVu Serif')
    ax.set_xlabel('Year', fontsize=18, fontname='DejaVu Serif')

    # Show all labels
    ax.set_xticks(x)
    ax.set_xticklabels(periods, rotation=45, ha='center', fontsize=16, fontname='DejaVu Serif')

    # Format y-axis to show values in thousands
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f'{int(x/1000)}'))
    ax.tick_params(axis='y', labelsize=16)
    
    # Professional styling
    ax.yaxis.grid(True, linestyle='--', linewidth=1.0, alpha=0.6)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Optimize layout
    plt.subplots_adjust(left=0.12, right=0.98, top=0.95, bottom=0.15)
    plt.tight_layout(pad=0.5)
    
    plt.savefig('total_commits_per_period.pdf', format='pdf', 
                bbox_inches='tight', pad_inches=0.1)
    plt.close()

def main():
    """Main function to execute the script."""
    if len(sys.argv) != 2:
        print("Usage: python total_commits_per_period.py <filename.csv>")
        sys.exit(1)
    
    filename = sys.argv[1]
    periods, total_commits = read_data(filename)
    plot_total_commits(periods, total_commits)
    print(f"Plot saved as 'total_commits_per_period.pdf'")

if __name__ == "__main__":
    main()