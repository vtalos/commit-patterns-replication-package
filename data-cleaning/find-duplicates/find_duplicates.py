"""
This script reads a list of projects from the "projects-accepted.txt" file. 
Each project is represented as a string that includes the repository name. The 
script identifies duplicate repositories (those that appear more than once) 
and outputs them in a sorted order based on a specified criterion. The output 
lists the duplicates with an enumerated index.
"""
# Open and read the file containing the project list
with open("projects-accepted.txt") as file:
    # Read all lines from the file and remove any trailing whitespace
    projects = file.readlines()
    projects = [project.strip() for project in projects]

# List to hold projects with duplicate repositories
duplicate_projects = []

# Dictionary to count occurrences of each repository
repo_count = {}

# Count the occurrences of each repository
for project in projects:
    repo = project.partition("/")[2]
    if repo in repo_count:
        repo_count[repo] += 1
    else:
        repo_count[repo] = 1

# Identify projects that have duplicate repositories
for i in range(0, len(projects)):
    repo = projects[i].partition("/")[2]
    if repo_count[repo] > 1:
        duplicate_projects.append(projects[i])

# Sort the duplicate projects based on the second element of the project string
sorted_projects = sorted(duplicate_projects, key=lambda project: project.split("/")[1])

# Output the sorted list of duplicate projects with an enumerated index
for i, project in enumerate(sorted_projects, 1):
    print(f"{i}. {project}")
