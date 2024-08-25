#!/bin/bash

set -eu
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github

> "$DATA_LOCATION/lines_per_developer.txt"

for year in {2004..2023}; do
    total_lines=0
    total_programmers=0

    while IFS= read -r name; do
        dir_name="$REPO_LOCATION/$name"
        cd "$dir_name" || continue
        
        # count only the inserted lines, not the deleted lines
        lines_per_project=$(git log --after="$((year-1))-12-31" --before="$((year+1))-01-01" --stat | grep -E 'insertions' | 
        awk '{insertions += $4} END {print insertions}')
        
        commits_per_project=$(git log --after="$((year-1))-12-31" --before="$((year+1))-01-01" --oneline | wc -l)
        programmers_per_project=$(git log --after="$((year-1))-12-31" --before="$((year+1))-01-01" --format='%aN' | sort -u | wc -l)
        
        total_lines=$((total_lines + lines_per_project))
        total_programmers=$((total_programmers + programmers_per_project))
        
        echo "name: $name year: $year lines_per_project: $lines_per_project commits_per_project: $commits_per_project programmers_per_project: $programmers_per_project"
    done < "$DATA_LOCATION/projects-accepted.txt"
    
    echo "year: $year total lines: $total_lines total commits: $total_commits total programmers: $total_programmers"
    
    # write the results about each project to the file
    average_lines_per_developer=$(echo "scale=2; $total_lines / $total_programmers" | bc)
    echo "$year: $average_lines_per_developer" >> "$DATA_LOCATION/lines_per_developer.txt"
done
