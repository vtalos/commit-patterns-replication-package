# Calculate Changes in FreeBSD Developer Age

* [`freebsd-age.bash`](freebsd-age.sh) calculates the average FreeBSD developer age in the end of 2007 (the year the developer list was added) and in the end of 2023.   
  Run `bash freebsd-age.bash <freeBSD_repo_directory>`

* [`committers-src.dot`](committers-src.dot) lists all FreeBSD src committers and describe the mentor-mentee relationships between them.

* [`most_used_timezone_per_year.py`](most_used_timezone_per_year.py) calculates the number of commits per year per timezone, excluding UTC-0.   
  Run `python most_used_timezone_per_year.py repos_path start_year end_year`

* [`demographics.py`](demographics.py) calculates the average number of years a contributor holds a commit bit.   
  Run `python demographics.py commiters-src.dot`