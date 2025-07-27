# Remove Inactive Repositories from Sample

* [`remove_inactive_repos.py`](remove_inactive_repos.py) identifies and removes repositories with last commit before 2015 from results.json in a single operation. Provides detailed output showing which repositories are being removed and statistics about the filtering process.   
  Run `python remove_inactive_repos.py`

* [`results.json`](results.json) contains repository data including metadata like commits, contributors, stars, forks, and timestamps. This file is cleaned in-place by the removal script.
