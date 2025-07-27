"""
This script randomly selects 355 unique repository names and writes the selected names to a text file.
Steps:
1. Loads data from 'results.json', expecting a dictionary with an "items" key containing item dictionaries.
2. Extracts the 'name' field from each item in the "items" list.
3. Randomly samples 355 unique names from the extracted list.
4. Writes the sampled names, one per line, to 'random_repos_sample.txt'.
"""
import json
import random

with open('results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    
items = [item['name'] for item in data["items"]]
random_sample = random.sample(items, 355)

with open('random_repos_sample.txt', 'w', encoding='utf-8') as file:
    for item in random_sample:
        file.write(f"{item}\n")