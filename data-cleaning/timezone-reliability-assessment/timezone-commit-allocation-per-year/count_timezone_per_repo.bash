#!/bin/bash
set -eu

declare -A commits_by_timezone
declare -a timezones

# Build timezone offsets array (-12 to +12)
for i in {0..24}; do
    offset=$((i - 12))
    if [ $offset -ge 0 ]; then
        timezone="+$(printf %02d $offset)00"
    else
        timezone="$(printf %03d $offset)00"
    fi
    timezones+=("$timezone")
done

DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github
OUTPUT_DIR="$DATA_LOCATION/timezones_per_repo"
SUMMARY_FILE="$DATA_LOCATION/most_common_timezones_summary.txt"

mkdir -p "$OUTPUT_DIR"
> "$SUMMARY_FILE"

# Map: most common timezone → repo count
declare -A timezone_repo_count

while IFS= read -r name; do
    dir_name="$REPO_LOCATION/$name"
    output_file="$OUTPUT_DIR/${name}.txt"
    > "$output_file"

    # Initialize/reset associative array for this repo
    for timezone_offset in "${timezones[@]}"; do
        commits_by_timezone["$timezone_offset"]=0
    done

    cd "$dir_name" || continue

    for timezone_offset in "${timezones[@]}"; do
        commits_count=$(git log --after="2003-12-31" --before="2024-01-01" | grep -- "$timezone_offset" | wc -l)
        commits_by_timezone["$timezone_offset"]=$commits_count
        echo "$timezone_offset: $commits_count" >> "$output_file"
    done

    # Find the most common timezone and its count
    max_count=0
    max_timezone=""
    for timezone_offset in "${timezones[@]}"; do
        count=${commits_by_timezone["$timezone_offset"]}
        if (( count > max_count )); then
            max_count=$count
            max_timezone=$timezone_offset
        fi
    done

    echo "" >> "$output_file"
    echo "Most common timezone: $max_timezone ($max_count commits)" >> "$output_file"

    # Record the most common timezone for this repo
    # Convert to UTC+ format for the summary
    formatted_tz="utc${max_timezone}"
    timezone_repo_count["$formatted_tz"]=$(( ${timezone_repo_count["$formatted_tz"]:-0} + 1 ))
done < "$DATA_LOCATION/projects-accepted.txt"

# Write summary file
for tz in "${!timezone_repo_count[@]}"; do
    echo "$tz: ${timezone_repo_count[$tz]}" >> "$SUMMARY_FILE"
done
