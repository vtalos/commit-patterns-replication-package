# Sampling

* [`ghs_results.csv`](ghs_results.csv) contains the repos of GHS sampling with at least 10 stars, 10 forks, 10 contributors and 12730 commits.
The sample is available at the web UI: http://seart-ghs.si.usi.ch, or directly from the replication package.

* [`repo_sampler.py`](repo_sampler.py) checks if the repos from `ghs_results.csv` have at least 20 years of commits and
every 6-month interval has at least (average number of commits per 6 months) / 5 commits.   
  Run `python repo_sampler.py ghs_results.csv <github_token>`
To run `repo_sampler.py` you need to obtain  a GitHub Personal Access Token  and provide it as an argument.

* [`projects-accepted.txt`](projects-accepted.txt) contains the projects that have been accepted by `repo_sampler.py`.

* [`fetch-projects.sh`](fetch-projects.sh) clone bare projects from  `projects-accepted.txt`.
