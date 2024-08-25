#!/bin/bash

# This script checks the number of commits with "git-svn-id" in the commit message for a given year and the next year for a list of repositories.
# It is used to detect and remove possible automated commits that are imported from SVN repositories.
# It takes the year as a command line argument.
# The script reads the list of repository names from the file "projects-accepted.txt" located in the same directory as the script.
# The repositories are assumed to be located in the directory "/home/repos/github".
# The script creates a file "check_git_svn_id.txt" in the current working directory to store the results.

# Usage: check_git_svn_id.bash <year>

# Parameters:
#   <year> - The year for which to check the commits with "git-svn-id" in the commit message.

# Example usage:
#   $ check_git_svn_id.bash 2021

# Example output in "check_git_svn_id.txt":
#   repository1: 10 5 5
#   repository2: 20 15 5
#   repository3: 5 10 -5

set -eu
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github
year=$1
> "$DATA_LOCATION/check_git_svn_id.txt"
echo "$year" >> "$DATA_LOCATION/check_git_svn_id.txt"

while IFS= read -r name; do
    dir_name="$REPO_LOCATION/$name"
    cd "$dir_name" || continue
    # count commits with "git-svn-id" in the commit message
    commits_with_git_svn=$(git log --after="$((year-1))-12-31" --before="$((year+1))-01-01" --grep="git-svn-id" --oneline | wc -l)
    # count commits with "git-svn-id" in the commit message for the next year
    commits_with_git_svn_next_year=$(git log --after="$year-12-31" --before="$((year+2))-01-01" --grep="git-svn-id" --oneline | wc -l)
    # calulate the difference
    diff=$((commits_with_git_svn - commits_with_git_svn_next_year))
    echo "$name: $commits_with_git_svn $commits_with_git_svn_next_year $diff"
    echo "$name: $commits_with_git_svn $commits_with_git_svn_next_year $diff" >> "$DATA_LOCATION/check_git_svn_id.txt"
done < "$DATA_LOCATION/projects-accepted.txt"
