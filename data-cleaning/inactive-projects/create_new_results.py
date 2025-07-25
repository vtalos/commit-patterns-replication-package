import json

with open('repos_to_be_removed.txt', 'r', encoding='utf-8') as file:
    repos_to_be_removed = file.read().splitlines()
with open('results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for item in data["items"]:
    if item['name'] in repos_to_be_removed:
        data["items"].remove(item)

with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)