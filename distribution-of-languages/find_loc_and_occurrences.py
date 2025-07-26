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
import json
from collections import defaultdict
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
loc = defaultdict(int)
occurance=[]   
with open ("results.json",encoding="utf-8") as file2:
    data = json.load(file2)
for row in data["items"]:
    if row["name"] in repos:
        language = row["mainLanguage"]
        if language:
            loc[language] += 1
            occurance.append(language)
        dicts_of_languages = row["metrics"]
        for lang in dicts_of_languages:
            loc[lang["language"]] += lang["codeLines"]
occurance_dict = count_unique_values(occurance)
languages = list(occurance_dict.keys())
for lang in languages:
    if lang not in loc.keys():
        del loc[lang]
sorted_loc = dict(sorted(loc.items(), key=lambda item: item[1], reverse=True))
sorted_occurance = dict(sorted(occurance_dict.items(), key=lambda item: item[1], reverse=True))
print(sorted_occurance)
print(sorted_loc)