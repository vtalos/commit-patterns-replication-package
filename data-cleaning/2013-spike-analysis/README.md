# Data Cleaning

* [`check_git_svn_id.bash`](check_git_svn_id.bash) checks the number of commits with "git-svn-id" in the commit message
for a given year and the next year for a list of repositories
run `check_git_svn_id.bash <year>`
* [`check_spike.bash`](check_spike.bash) This script analyzes the spike in commits made between 23:00-23:59 for a specific year.
run `check_spike.bash <year>`
* [`find-rejected-mariadb-commits.bash`](find-rejected-mariadb-commits.bash)  counts false mariadb commits
run `find-rejected-mariadb-commits.bash`
* [`check_git_svn_id.txt'](check_git_svn_id.txt-projects.txt) contains the number of commits containing 'git-svn-id' for a year,
compared to the next year(2013 in that file)
* [`check_spike.txt'](check_spike.txt) contains the number of commits, commits next year, and the difference between the two years for each project for 23:00-23:59,
as well as the total number of commits for the rest of the day (2013 in that file).