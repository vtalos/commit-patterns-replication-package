# Contributors' Number

* [`projects-accepted.txt`](projects-accepted.txt) contains the projects that have been accepted by `../sampling/repo_sampler.py` and has not a duplicate name.

* [`all_contributors_per_year.bash`](all_contributors_per_year.bash) counts the summation of contributors for all projects of the sample, for 2004-2023, and creates `all_contributors_per_year.txt` file.   
  Run `bash all_contributors.bash`

* [`all_contributors_per_year.txt`](all_contributors_per_year.txt) contains the number of contributors for each year of the sample obtained from `all_contributors.bash`, including rejected commits due to bad timestamps.

* [`contributors_plot.py`](contributors_plot.py) visualizes the content of `all_contributors_per_year.txt` using matplotlib.   
  Run `python contributors_plot.py all_contributors_per_year.txt`
