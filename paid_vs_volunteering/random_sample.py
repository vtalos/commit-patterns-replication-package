import json
import random

with open('results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    
items = [item['name'] for item in data["items"]]
random_sample = random.sample(items, 355)

with open('random_repos_sample.txt', 'w', encoding='utf-8') as file:
    for item in random_sample:
        file.write(f"{item}\n")