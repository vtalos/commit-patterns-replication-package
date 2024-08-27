# Number of Lines per Language

* [`count_lines_per_language.py`](`count_lines_per_language.py`) automates the process of generating and aggregating line-of-code (LOC) statistics for the sample. providing a summary of the total number of files, blank lines, comment lines, and code lines per programming language across all the projects.
    Run `python count_lines_per_language.py`

* [`projects-accepted.txt`](projects-accepted.txt) contains the projects that have been accepted by `../sampling/repo_sampler.py` and is not duplicate.

* [`fetch-projects.sh`](fetch-projects.sh) clones projects from  `projects-accepted.txt` but does not use --bare.
    Run `bash fetch-projects.sh`