#!/bin/bash
# This script counts how many commits were made in 
# each timezone for a given year

set -eu

#associative array to store commits count by timezone
declare -A commits_by_timezone
#array to store timezone offsets
declare -a timezones

#create array for the year in the arguements
arguements=("$@")

for i in {0..24}; do
    offset=$((i - 12))
    # Format offset with leading zeroes if needed
    if [ $offset -ge 0 ]; then
        timezone="+$(printf %02d $offset)00"
    else
        timezone="$(printf %03d $offset)00"
    fi
    #append in array
    timezones+=("$timezone")
done

DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github

for year in ${arguements[@]}; do
	echo "$year" >> "$DATA_LOCATION/commits_by_timezone_$year.txt"
	#initialize commits_by_timezone array
	for timezone_offset in ${timezones[@]}; do
    		commits_by_timezone["$timezone_offset"]=0
	done
	#Loop through projects
	while IFS= read -r name; do
    		dir_name="$REPO_LOCATION/$name"
    		cd "$dir_name" || continue

    		# Loop through timezone offsets from -12 to +12
    		for timezone_offset in ${timezones[@]}; do
    		# Execute git log command with timezone offset
    		commits_count=$(git log --after="$((year-1))-12-31" --before="$((year+1))-01-01" | grep -- "$timezone_offset" | wc -l)
    		commits_by_timezone["$timezone_offset"]=$(( ${commits_by_timezone["$timezone_offset"]} + commits_count ))
    		echo "$name: $timezone_offset: $commits_count"
    		done 
	done < "$DATA_LOCATION/projects-accepted.txt"
	# write results to the  file
	for timezone_offset in ${timezones[@]}; do
    		echo "$timezone_offset: ${commits_by_timezone["$timezone_offset"]}" >> "$DATA_LOCATION/commits_by_timezone_$year.txt"
	done
done