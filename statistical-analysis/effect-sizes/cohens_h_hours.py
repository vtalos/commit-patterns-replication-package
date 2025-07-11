"""
This script calculates Cohen's h, a measure of effect size, between two years for a specific hour block
based on commit percentages provided in a CSV file.

The script reads the commit percentages for a specified time block (defined by start and end hours) and
two years from the CSV file. It then calculates Cohen's h to quantify the difference in commit percentages
between these years.

Usage:
    python cohens_h_hours.py <filename.csv> <start_hour> <end_hour> <first_period> <second_period>

Cohen's h is interpreted as:
- Small effect size if h < 0.2
- Medium effect size if h < 0.5
- Large effect size if h >= 0.5

Arguments:
- filename: The CSV file to get the data from.
- start_hour: The starting hour of the time block (24-hour format).
- end_hour: The ending hour of the time block (24-hour format).
- year1: The first year to compare.
- year2: The second year to compare.

Usage example:
python cohens_h_hours.py CommitPercentagesPerHour.csv 9 17 2015 2024
"""
import sys
import argparse
import csv
import math

def calculate_cohens_h(p1, p2):
    # Convert percentages to proportions
    p1 = p1 / 100
    p2 = p2 / 100
    # Calculate Cohen's h
    h = 2 * (math.asin(math.sqrt(p1)) - math.asin(math.sqrt(p2)))
    return h

def get_commit_percentage_sum(filename, year, start_hour, end_hour):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        year_index = header.index(str(year))
        start_hour = int(start_hour)
        end_hour = int(end_hour)
        
        total_commits = 0

        for row in reader:
            hour = int(row[0].split(':')[0])
            if start_hour <= end_hour:
                if start_hour <= hour < end_hour:
                    total_commits += float(row[year_index])
            else:
                if hour >= start_hour or hour < end_hour:
                    total_commits += float(row[year_index])

        return total_commits

def main():
    parser = argparse.ArgumentParser(description="A script for calculating Cohen's h between two time periods for a specific hour block")
    
    parser.add_argument("filename", help="The CSV file to get the data from")
    parser.add_argument("start_hour", help="The starting hour (24-hour format)")
    parser.add_argument("end_hour", help="The ending hour (24-hour format)")
    parser.add_argument("year1", help="The first year")
    parser.add_argument("year2", help="The second year")
    
    args = parser.parse_args()
    
    filename = args.filename
    start_hour = args.start_hour
    end_hour = args.end_hour
    year1 = args.year1
    year2 = args.year2
    
    # Get commit percentages for the specified years and hour block
    p1 = get_commit_percentage_sum(filename, year1, start_hour, end_hour)
    p2 = get_commit_percentage_sum(filename, year2, start_hour, end_hour)
    
    if p1 is None or p2 is None:
        print("Error: Unable to find data for the specified periods and hour block.")
        sys.exit(1)
    
    # Calculate Cohen's h
    h = calculate_cohens_h(p1, p2)
    
    # Print results
    print(f"Total commit percentage for {start_hour}:00 to {end_hour}:00 in {year1}: {p1:.2f}%")
    print(f"Total commit percentage for {start_hour}:00 to {end_hour}:00 in {year2}: {p2:.2f}%")
    print(f"Cohen's h: {h:.4f}")
    
    # Interpret the results
    if abs(h) < 0.2:
        interpretation = "small effect size"
    elif abs(h) < 0.5:
        interpretation = "medium effect size"
    else:
        interpretation = "large effect size"
    
    print(f"The change in commit percentage from {year1} to {year2} for {start_hour}:00 to {end_hour}:00 represents a {interpretation}.")

if __name__ == "__main__":
    main()