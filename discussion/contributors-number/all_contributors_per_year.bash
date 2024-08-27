#!/bin/bash
# This script counts the number of contributors per year for all the projects in the projects-accepted.txt file
set -eu
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github
for year in {2004..2023}; do
    contributors_per_year_all_repos=0 
    while IFS= read -r name ; do
        contributors_per_year=0  
        dir_name="$REPO_LOCATION/$name"	
        cd "$dir_name" || continue
        contributors_per_year=$(git log --after="$year-01-01" --before="$year-12-31" --format='%ae' | sort -u | wc -l) 
        contributors_per_year_all_repos=$((contributors_per_year_all_repos + contributors_per_year)) 
    done <"$DATA_LOCATION/projects-accepted.txt"
    echo "$year: $contributors_per_year_all_repos"
    echo "$year: $contributors_per_year_all_repos" >> "$DATA_LOCATION/all_contributors_per_year.txt" 
done
