import json
import datetime

print("Loading repository data...")
with open('results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

print(f"Total repositories before filtering: {len(data['items'])}")

# Filter out inactive repositories (last commit before 2015)
active_repos = []
inactive_count = 0

for item in data["items"]:
    created_at = datetime.datetime.strptime(item.get('createdAt', ''), '%Y-%m-%dT%H:%M:%S')
    last_commit = datetime.datetime.strptime(item.get('lastCommit', ''), '%Y-%m-%dT%H:%M:%S')
    
    if last_commit.year >= 2015:
        active_repos.append(item)
    else:
        inactive_count += 1
        print(f"Removing inactive repo: {item['name']} (last commit: {last_commit.year})")

print(f"\nRepositories removed: {inactive_count}")
print(f"Active repositories remaining: {len(active_repos)}")

# Update the data with only active repositories
data["items"] = active_repos

# Write the cleaned results back to the file
print("Writing cleaned results.json...")
with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("✓ Inactive repositories have been removed from results.json")
