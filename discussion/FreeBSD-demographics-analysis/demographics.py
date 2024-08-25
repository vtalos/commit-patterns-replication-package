"""
Script to calculate the average years an active contributor of FreeBSD
holds a commit bit.

Description:
    This script analyzes a dot file containing data about alumni and active
    committers of FreeBSD to calculate the average number of years a contributor
    holds a commit bit, providing insights into project engagement over time.

Usage:
    demographics.py <commiters-src.dot>

Arguments:
    <commiters-src.dot>: A dot file containing information about alumni and active
                         committers of FreeBSD.

Returns:
    Average number of years a contributor holds a commit bit.

Dependencies:
    - matplotlib
    - sys

Example:
    python demographics.py commiters-src.dot
"""


from datetime import datetime
import sys

def calculate_active_years(commit_date):
    today = datetime.now()
    commit_date = datetime.strptime(commit_date, "%Y/%m/%d")
    age_difference = today - commit_date
    return age_difference.days/365.25  #Return the active years in project. Include leap years

filename=sys.argv[1]

# Read data from the file
with open('committers-src.dot', 'r') as file:
    #read only active contributors
    lines = file.readlines()[100:396]

# Extract commit dates from the file
commit_dates = []
for line in lines:
    if "label" in line:
        try:
            commit_date = line.split("\\n")[2].split('"')[0] #extract date
        except: #handle bad date format
            commit_date = line.split("@FreeBSD.org\\n")[1].split('"')[0]
        if'?' not in commit_date and '/' in commit_date: #ignore invalid dates
            commit_dates.append(commit_date)

# Calculate commit bit hold duration and store in a list
ages = [calculate_active_years(commit_date) for commit_date in commit_dates]

# Calculate average commit bit hold duration
average_age = sum(ages) / len(ages)

print("Average number of years a contributor holds a commit bit:", round(average_age, 2))