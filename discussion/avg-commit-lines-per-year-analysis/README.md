# Average Inserted Lines per Commit Analysis

* [`projects-accepted.txt`](projects-accepted.txt) contains the projects that have been accepted by `../sampling/repo_sampler.py` and has not a duplicate name.

* [`lines_per_commit.bash`](lines_per_commit.bash) counts the number of lines per commit for each year for all the projects in the projects-accepted.txt file.   
  Run `bash lines_per_commit.bash`

* [`lines_per_commit.txt`](lines_per_commit.txt) contains the number of lines per commit for each year for all the projects in the projects-accepted.txt file.

* [`lines_per_commit_plot.py`](lines_per_commit_plot.py) visualizes the content of lines_per_commit.txt using Matplotlib.   
  Run `python lines_per_commit_plot.py`
