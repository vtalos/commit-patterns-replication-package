# Paid vs Volunteering Analysis

* [`random_sample.py`](random_sample.py) generates a random sample of 355 repositories from results.json and writes their names to random_repos_sample.txt.   
  Run `python random_sample.py`

* [`random_repos_sample.txt`](random_repos_sample.txt) contains the random sample of repository names with classification labels (company/volunteering) in repository_name, label format.

* [`results.json`](results.json) contains the repositories of GHS sampling with at least 10 stars, 10 forks, 10 contributors and 12730 commits, along with the metadata used for sampling.

* [`enterprise_projects.txt`](enterprise_projects.txt) contains a dataset of open source software developed mainly by enterprises rather than volunteers from https://zenodo.org/records/3742962.

* [`cohort_project_details.txt`](cohort_project_details.txt) contains a dataset of cohort projects that are not part of the enterprise data set, but have comparable quality attributes from https://zenodo.org/records/3742962.

* [`find_enterprise_projects.py`](find_enterprise_projects.py) finds the repositories from our sample that are either in `enterprise_projects.txt` or `cohort_project_details.txt`.
Run `python find_enterprise_projects.py`