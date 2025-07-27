import json
from collections import defaultdict

with open("results.json", "r", encoding="utf-8") as file:
    data = json.load(file)

last_commits_per_project = defaultdict(int)
active_repos_per_year = defaultdict(int)

for row in data["items"]:
    last_commit_year = row["lastCommit"].split("-")[0]
    created_at_year = row["createdAt"].split("-")[0]
    for year in range(int(created_at_year), int(last_commit_year) + 1):
        active_repos_per_year[year] += 1
    last_commits_per_project[last_commit_year] += 1

# Sort the dictionary by year
last_commits_per_project = dict(sorted(last_commits_per_project.items()))
print(last_commits_per_project)
number_of_projects = sum(last_commits_per_project.values())
print(active_repos_per_year)

with open("active_repos_per_year.txt", "w") as f:
    for year, count in active_repos_per_year.items():
        f.write(f"{year},{count}\n")