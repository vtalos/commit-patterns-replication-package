import csv

"""
Repository Language Analyzer

This script counts the number of repositories per programming language for the accepted projects.

Requirements:
    - Python 3.x

Input Files:
    - projects-accepted.txt: Text file with one repository name per line.
    - ghs_results.csv: CSV file with repository details, where:
        - Column 2 (row[1]) contains repository names.
        - Column 8 (row[7]) contains the main programming language.

Output:
    - Prints a dictionary showing the count of repositories per programming language.

Example Output:
    {'Python': 15, 'JavaScript': 7, 'Java': 3, 'Ruby': 2}
"""

def count_unique_values(list):
    count_dict = {}
    for item in list:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    return count_dict

repos=[]
with open("projects-accepted.txt") as file1:
    lines = file1.readlines()
    for line in lines:
        repos.append(line.strip())
      
occurance=[]   
with open ("ghs_results.csv") as file2:
    reader = csv.reader(file2)
    next(reader)
    for row in reader:
            #if repo is in accepted projects
            if row[1] in repos:
                #add the programming language of project
                occurance.append(row[7])
occurance_dict = count_unique_values(occurance)
print(occurance_dict)