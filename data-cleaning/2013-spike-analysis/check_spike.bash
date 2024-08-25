#!/bin/bash
# This script analyzes the spike in commits made between 23:00-23:59 for a specific year.
# It is used to detect and remove possible automated commits or anomalies.
# It reads a list of project names from the "projects-accepted.txt" file and calculates the number of commits made between 23:00-23:59 for the given year and the previous year.
# Outputs the number of commits, commits next year, and the difference between the two years for each project, as well as the total number of commits for the rest of the day.

# Usage: check_spike.bash <year>

# Parameters:
#   <year> - The year for which to analyze the spike in commits.

# Example usage: check_spike.bash 2013

# Example output:
# 2013
# commits, commits next year, difference, commits rest of the day
# project1: 10 5 5 40
# project2: 8 3 5 30
# ...
# total commits 23:00-23:59 130 total diff 200 total commits rest day 270
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
