# Paid vs Volunteering Analysis

* [`random_sample.py`](random_sample.py) generates a random sample of 355 repositories from results.json and writes their names to random_repos_sample.txt.   
  Run `python random_sample.py`

* [`random_repos_sample.txt`](random_repos_sample.txt) contains the random sample of repository names with classification labels (company/volunteering) in repository_name,classification format.

* [`results.json`](results.json) contains the repositories of GHS sampling with at least 10 stars, 10 forks, 10 contributors and 12730 commits, along with the metadata used for sampling.