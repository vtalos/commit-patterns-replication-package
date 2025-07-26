# Number of Repositories and Lines of Code per Language

* [`find_loc_and_occurrences.py`](find_loc_and_occurrences.py) counts the number of repositories and lines of code per programming language for the accepted projects by analyzing results.json and projects-accepted.txt.   
  Run `python find_loc_and_occurrences.py`

* [`find_last_commits_per_project.py`](find_last_commits_per_project.py) analyzes repository activity by calculating the number of active repositories per year based on creation and last commit dates. Outputs data to active_repos_per_year.txt.

* [`projects-accepted.txt`](projects-accepted.txt) contains the projects that have been accepted in the sample.

* [`active_repos_per_year.txt`](active_repos_per_year.txt) contains the count of active repositories per year in year,count format.

* [`results.json`](results.json) contains the repositories of GHS sampling with at least 10 stars, 10 forks, 10 contributors and 12730 commits, along with the metadata that will be used in `find_loc_and_occurrences.py`.
The sample is available at the web UI: http://seart-ghs.si.usi.ch, or directly from the replication package.