# Find Inactive Repos in the Sample

* [`find_inactive_repos.py`](find_inactive_repos.py) identifies repositories with last commit before 2015 from results.json and writes their names to repos_to_be_removed.txt.

* [`create_new_results.py`](create_new_results.py) creates a new results.json that does not contain the inactive repos.
Run `python create_new_results.py`

* [`results.json`](results.json) contains repository data including metadata like commits, contributors, stars, forks, and timestamps.

