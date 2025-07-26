# Sampling

* [`ghs_results.csv`](ghs_results.csv) contains the repos of GHS sampling with at least 10 stars, 10 forks, 10 contributors and 12730 commits.
The sample is available at the web UI: http://seart-ghs.si.usi.ch, or directly from the replication package.

* [`csv_to_repos_list.py`](csv_to_repos_list.py) extracts repository names from ghs_results.csv and saves them to projects-accepted.txt.   
  Run `python csv_to_repos_list.py`

* [`repo_information_scraper.py`](repo_information_scraper.py) scrapes GitHub repository information using the GitHub REST API for repositories from a text file. Requires optional GitHub token for higher rate limits.

* [`find_deleted_repos.py`](find_deleted_repos.py) checks for deleted or inaccessible repositories from projects-accepted.txt using GitHub API and filters out non-existent repos. Requires GitHub token via GH_TOKEN environment variable.

* [`projects-accepted.txt`](projects-accepted.txt) contains the list of accepted repository names extracted from the sampling process.

* [`final_repos_selected_info.csv`](final_repos_selected_info.csv) contains detailed information about the final selected repositories including size, contributors, commits, stars, language, and classification (volunteering/corporate).

* [`fetch-projects.sh`](fetch-projects.sh) clones or refreshes Git repositories from projects-accepted.txt to a local directory.
  Run `sh fetch-projects.sh`
