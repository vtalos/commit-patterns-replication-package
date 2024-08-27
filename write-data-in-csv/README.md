# Write Data in CSV

* [`commit_count_per_day.py`](commit_count_per_day.py): Creates a CSV containing commit counts per day of the week for a given interval and repository.
  - For total counts run `python commit_count_per_day.py <start_year> <end_year> <interval> total <repos_file.txt> <cloned_repos_path>`
  - For proportions run `python commit_count_per_day.py <start_year> <end_year> <interval> proportions <repos_file.txt> <cloned_repos_path>`

* [`commit_count_per_hour.py`](commit_count_per_hour.py): Creates a CSV containing the commit count per hour for a given interval and repository.
  - For total counts run `python commit_count_per_hour.py <start_year> <end_year> <interval> total <repos_file.txt> <cloned_repos_path>`
  - For proportions run `python commit_count_per_hour.py <start_year> <end_year> <interval> proportions <repos_file.txt> <cloned_repos_path>`
