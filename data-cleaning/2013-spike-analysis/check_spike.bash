#!/bin/bash
# This script counts the number of commits in a specific hour and year
# for all the projects in the projects-accepted.txt file
set -eu
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github

> "$DATA_LOCATION/check_spike.txt"
total_commits_at_23=0
total_diff=0
year=$1
echo "$year" >> "$DATA_LOCATION/check_spike.txt"
echo "commits, commits next year, difference" >> "$DATA_LOCATION/check_spike.txt"
while IFS= read -r name; do
        dir_name="$REPO_LOCATION/$name"
        cd "$dir_name" || continue
        # count commints inside 23:00-23:59 for the specific year
        commits_at_23=$(git log --after="$((year-1))-12-31" --before="$((year+1))-01-01"  | grep Date |
        awk '{ print $5 }' | awk '/^23/' | wc -l)
        #count commits inside 23:00-23:59 for the previous year
        commits_at_23_last_year=$(git log --after="$((year-2))-12-31" --before="$((year))-01-01"  | grep Date |
        awk '{ print $5 }' | awk '/^23/' | wc -l)
        #calculate the difference between the two years for 23:00-23:59
        diff=$((commits_at_23 - commits_at_23_last_year))
	total_commits_at_23=$((commits_at_23 + total_commits_at_23))
	total_diff=$((diff + total_diff))
        echo "$name: $commits_at_23 $commits_at_23_last_year $diff" >> "$DATA_LOCATION/check_spike.txt"
done < "$DATA_LOCATION/projects-accepted.txt"
echo "total commits 23:00-23:59 $total_commits_at_23 total diff $total_diff" >> "$DATA_LOCATION/check_spike.txt" 
