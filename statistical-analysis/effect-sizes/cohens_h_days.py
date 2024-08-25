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

def get_commit_percentage(filename, period, day):
    day_index = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }
    
    index = day_index[day]
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        period_index = header.index(period)
        for row in reader:
            if reader.line_num == index + 2:  # The data for each day starts from the second row
                return float(row[period_index])
    return None

def main():
    parser = argparse.ArgumentParser(description="A script for calculating Cohen's h between two time periods for a specific day")
    
    parser.add_argument("filename", help="The CSV file to get the data from")
    parser.add_argument("period1", help="The first time period")
    parser.add_argument("period2", help="The second time period")
    parser.add_argument("day", help="The day of the week")
    
    args = parser.parse_args()
    
    filename = args.filename
    period1 = args.period1
    period2 = args.period2
    day = args.day
    
    # Get commit percentages for the specified periods and day
    p1 = get_commit_percentage(filename, period1, day)
    p2 = get_commit_percentage(filename, period2, day)
    
    if p1 is None or p2 is None:
        print("Error: Unable to find data for the specified periods and day.")
        sys.exit(1)
    
    # Calculate Cohen's h
    h = calculate_cohens_h(p1, p2)
    
    # Print results
    print(f"Commit percentage for {day} in {period1}: {p1}%")
    print(f"Commit percentage for {day} in {period2}: {p2}%")
    print(f"Cohen's h: {h:.4f}")
    
    # Interpret the results
    if abs(h) < 0.2:
        interpretation = "small effect size"
    elif abs(h) < 0.5:
        interpretation = "medium effect size"
    else:
        interpretation = "large effect size"
    
    print(f"The change in commit percentage from {period1} to {period2} for {day} represents a {interpretation}.")

if __name__ == "__main__":
    main()