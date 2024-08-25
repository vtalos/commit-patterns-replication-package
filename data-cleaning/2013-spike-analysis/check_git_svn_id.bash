#!/bin/bash
# This script counts the number of commits with "git-svn-id" in the commit
# message for the year selected and the next
# for all the projects in the projects-accepted.txt file.

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
