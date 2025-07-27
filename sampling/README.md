# Sampling

* [`ghs_results.csv`](ghs_results.csv) contains the repos of GHS sampling with at least 10 stars, 10 forks, 10 contributors and 12730 commits.
The sample is available at the web UI: http://seart-ghs.si.usi.ch, or directly from the replication package.

* [`extract_and_validate_repos.py`](extract_and_validate_repos.py) extracts repository names from ghs_results.csv and validates that they are still accessible on GitHub, filtering out deleted or inaccessible repositories. Combines extraction and validation in a single efficient operation. Requires optional GH_TOKEN environment variable for higher rate limits.   
  Run `python extract_and_validate_repos.py`

* [`repo_information_scraper.py`](repo_information_scraper.py) scrapes GitHub repository information using the GitHub REST API for repositories from a text file. Requires optional GitHub token for higher rate limits.

* [`projects-accepted.txt`](projects-accepted.txt) contains the list of validated repository names that are confirmed to exist on GitHub.

* [`final_repos_selected_info.csv`](final_repos_selected_info.csv) contains detailed information about the final selected repositories including size, contributors, commits, stars, language, and classification (volunteering/corporate).

* [`fetch-projects.sh`](fetch-projects.sh) clones or refreshes Git repositories from projects-accepted.txt to a local directory.
  Run `sh fetch-projects.sh`
