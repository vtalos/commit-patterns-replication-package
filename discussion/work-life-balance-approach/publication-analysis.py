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