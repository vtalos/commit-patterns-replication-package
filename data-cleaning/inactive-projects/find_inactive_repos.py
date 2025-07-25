import json
from collections import defaultdict
import datetime

repos_to_be_removed = []
with open('results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
for item in data["items"]:
    created_at = datetime.datetime.strptime(item.get('createdAt', ''), '%Y-%m-%dT%H:%M:%S')
    last_commit = datetime.datetime.strptime(item.get('lastCommit', ''), '%Y-%m-%dT%H:%M:%S')
    if last_commit.year < 2015:
        repos_to_be_removed.append(item['name'])
with open('repos_to_be_removed.txt', 'w', encoding='utf-8') as file:
    for repo in repos_to_be_removed:
        file.write(f"{repo}\n")