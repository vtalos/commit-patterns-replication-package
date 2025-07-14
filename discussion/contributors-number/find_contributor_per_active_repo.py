with open("active_repos_per_year.txt", "r") as f:
    data = f.readlines()
active_repos_per_year = {}
for line in data:
    year, count = line.strip().split(',')
    active_repos_per_year[int(year)] = int(count)

with open("all_contributors_per_year.txt", "r") as f:
    data = f.readlines()
all_contributors_per_year = {}
for line in data:
    year, count = line.strip().split(':')
    all_contributors_per_year[int(year)] = int(count)

for year in range(2015, 2025):
    print(f"{year}: {round(all_contributors_per_year.get(year, 0)/ active_repos_per_year.get(year, 1),0)} contributors per active repo")