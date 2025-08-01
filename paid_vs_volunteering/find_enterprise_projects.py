import json

with open('enterprise_projects.txt', 'r', encoding='utf-8') as file:
    data = file.readlines()
projects = [line.strip().split('\t')[0].split('/')[-2:] for line in data]
projects = [f"{name}/{repo}" for name, repo in projects]
set_projects = set(projects)

with open('cohort_project_details.txt', 'r', encoding='utf-8') as file:
    projects2 = file.readlines()
projects2 = [line.strip().split('\t')[0].split('/')[-2:] for line in projects2]
projects2 = [f"{name}/{repo}" for name, repo in projects2]
set_projects2 = set(projects2)

with open('results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

projects_in_sample = set(item['name'] for item in data['items'])

enterprise_in_sample = set_projects.intersection(projects_in_sample)
print(f"Enterprise projects in sample: {len(enterprise_in_sample)}")

cohort_in_sample = set_projects2.intersection(projects_in_sample)
print(f"Project with enterprise-like attributes: {len(cohort_in_sample)}")