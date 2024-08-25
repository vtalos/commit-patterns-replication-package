"""
cloc Aggregator Script
======================

This script automates the process of generating and aggregating line-of-code (LOC) statistics 
for the sample. It uses the `cloc` (Count Lines of Code) tool to analyze the 
source code in each project and outputs a CSV file containing statistics for each project. 
The script then reads these CSV files and aggregates the results, providing a summary of 
the total number of files, blank lines, comment lines, and code lines per programming language 
across all the projects.

Requirements:
-------------
- Python 3.x
- `cloc` command-line tool (must be installed and available in your system's PATH)

Directory Structure:
--------------------
- `projects-accepted-revised.txt`: A text file containing a list of project paths relative 
  to the `REPO_LOCATION` directory. Each line should correspond to one project.

- `REPO_LOCATION`: The base directory where the repositories are located.


Usage:
------
1. Use the list of projects in a text file named `projects-accepted-revised.txt`.
2. Set the `REPO_LOCATION` variable to the directory containing the projects.
3. Run the script.
4. The script will generate a CSV file for each project in the current working directory.
5. After processing all projects, the script will output aggregated statistics for all 
   languages found across the projects.

Output:
-------
The script outputs the aggregated line-of-code statistics to the console, summarizing the 
total number of files, blank lines, comment lines, and code lines per programming language 
across all the processed projects.
"""

import csv
from collections import defaultdict
import os
import subprocess

def find_last_commit_of_2023(project):
    # Find the last commit of 2023
    last_commit = None
    path = os.path.join(REPO_LOCATION, project.strip())
    try:
        # Run git log to find the last commit's of 2023 SHA
        last_commit = subprocess.run(
            ["git", "log", "--before=2024-01-01", "--max-count=1", "--format=%H"],
            check=True,  # This raises an error if git log fails
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running git log on {path}: {e}")
    return last_commit

def create_csv_file(project,hash):
    path = os.path.join(REPO_LOCATION, project.strip())
    try:
        # Change to the project's directory
        os.chdir(path)
        # Checkout the specific commit using the provided hash
        subprocess.run(["git", "checkout", hash], check=True)
        # Run cloc and save the output to a CSV file
        subprocess.run(
            ["cloc", path, "--csv", f"--out={project.split('/')[1]}.csv"],
            check=True  # This raises an error if cloc fails
        )
        csv_files.append(f"{project.split('/')[1]}.csv")
        print(f"CSV for {path} created successfully.")
        return project.split('/')[1] + ".csv"
    except subprocess.CalledProcessError as e:
        print(f"Error running cloc on {path}: {e}")
    return None

def calculate_lines_per_language(csv_files):
    total_counts = defaultdict(lambda: {"files": 0, "blank": 0, "comment": 0, "code": 0})
    for file in csv_files:
        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lang = row['language']
                total_counts[lang]["files"] += int(row['files'])
                total_counts[lang]["blank"] += int(row['blank'])
                total_counts[lang]["comment"] += int(row['comment'])
                total_counts[lang]["code"] += int(row['code'])
    return total_counts

REPO_LOCATION= os.getcwd()
total_counts = defaultdict(lambda: {"files": 0, "blank": 0, "comment": 0, "code": 0})
csv_files=[]
with open('projects-accepted-revised.txt', 'r') as f:
        projects = f.readlines()
        for project in projects:
            project = project.strip()
            commit_hash = find_last_commit_of_2023(project)
            csv_files.append(create_csv_file(project,commit_hash))
total_counts = calculate_lines_per_language(csv_files)

for lang, counts in total_counts.items():
    print(f"{lang}: {counts}")