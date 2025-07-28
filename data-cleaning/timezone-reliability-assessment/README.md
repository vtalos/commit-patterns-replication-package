# Timezone Reliability Assessment

This directory contains scripts to analyze timezone patterns in commit data to assess the reliability and distribution of commits across different timezones.

## Core Analysis Scripts

* [`count_all_timezone_commits.bash`](count_timezone_commits.bash) counts **all commits** made in each timezone for specified years. Provides a comprehensive view of timezone distribution without filtering.   
    Run `bash count_timezone_commits.bash <year1> [year2] [year3]...`

* [`analyze_filtered_timezone_commits.py`](find_commits_per_timezone.py) counts commits from **contributors who have made at least one non-UTC commit**, filtering out likely automated/CI commits to focus on human developer patterns. Processes a date range across multiple years.   
    Run `python find_commits_per_timezone.py <start_year> <end_year> <repos_file> <repos_path>`


## Statistical Analysis

* [`calculate_yearly_timezone_variations.py`](early_year_variations.py) analyzes commit data from text files to calculate timezone distribution metrics including standard deviation, coefficient of variation, entropy, and UTC+0000 percentage for each year.   
    Run `python early_year_variations.py`

## Data Files

* [`projects-accepted.txt`](projects-accepted.txt) contains the list of accepted repository names used by the analysis scripts.

