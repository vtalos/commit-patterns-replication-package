# Write Data in CSV

* [`commit_count_per_day.py`](commit_count_per_day.py): Creates a CSV containing commit counts per day of the week for a given interval and repository.
  - For total counts run `python3 commit_count_per_day.py start_year end_year interval total repo_names_file cloned_repos_path`.
  - For proportions run `python3 commit_count_per_day.py start_year end_year interval proportions repo_names_file cloned_repos_path`

* [`commit_count_per_hour.py`](commit_count_per_hour.py): Creates a CSV containing the commit count per hour for a given interval and repository.
  - For total counts run `python3 commit_count_per_hour.py start_year end_year interval total repo_names_file cloned_repos_path`.
  - For proportions run `python3 commit_count_per_hour.py start_year end_year interval proportions repo_names_file cloned_repos_path`
