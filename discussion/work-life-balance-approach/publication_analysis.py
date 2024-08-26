"""
This script reads data from two CSV files, calculates the percentage increase in publications year-over-year for both total publications and work-life balance-related publications, and then compares their average percentage increases.

The script performs the following steps:
1. **Read and Process Data:** 
   - Reads the data from `total_publications.csv` and `work_life_balance_publications.csv`.
   - Stores the number of publications for each year in reversed order (i.e., from oldest to newest).

2. **Calculate Percentage Increase:**
   - Calculates the year-over-year percentage increase in publications for both total publications and work-life balance publications.

3. **Calculate Average Percentage Increase:**
   - Computes the average percentage increase over the entire time period for both sets of publications.

4. **Compare and Output Results:**
   - Prints the average percentage increase for each category.
   - Compares the two averages and prints which category shows a bigger average percentage increase.

Assumptions:
- The second column of the CSV files contains the number of publications for each year.

Output:
- Average percentage increase for total publications.
- Average percentage increase for work-life balance publications.
- A comparison of the two averages.

Usage:
Simply run the script. Ensure the CSV files `total_publications.csv` and `work_life_balance_publications.csv` are in the same directory as the script.
"""
import csv

# Initialize a list to hold the data
total_list = []
wlb_list = []

# Read the CSV file and populate the data list
with open('total_publications.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    # Skip 8 rows
    for _ in range(8):
        next(csvreader)

    for row in csvreader:
        total_list.append(row)

    total_publications = []

    for year in total_list:
        total_publications.insert(0,int(year[1]))


# Read the CSV file and populate the data list
with open('work_life_balance_publications.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    # Skip 8 rows
    for _ in range(8):
        next(csvreader)

    for row in csvreader:
        wlb_list.append(row)

    work_life_balance_publications = []

    for year in wlb_list:
        work_life_balance_publications.insert(0,int(year[1]))

# Calculate percentage increase for each list
total_increase = [(total_publications[i+1] - total_publications[i]) / total_publications[i] * 100 for i in range(len(total_publications)-1)]
work_life_balance_increase = [(work_life_balance_publications[i+1] - work_life_balance_publications[i]) / work_life_balance_publications[i] * 100 for i in range(len(work_life_balance_publications)-1)]

# Calculate average percentage increase for each list
avg_total_increase = sum(total_increase) / len(total_increase)
avg_work_life_balance_increase = sum(work_life_balance_increase) / len(work_life_balance_increase)

# Print average percentage increase for each list
print(f"Average percentage increase for total publications: {avg_total_increase:.2f}%")
print(f"Average percentage increase for work-life balance publications: {avg_work_life_balance_increase:.2f}%")

# Compare the average percentage increase
if avg_total_increase > avg_work_life_balance_increase:
    print("Total publications show a bigger average percentage increase.")
elif avg_work_life_balance_increase > avg_total_increase:
    print("Work-life balance publications show a bigger average percentage increase.")
else:
    print("Both lists show equal average percentage increase.")