# Replication Package for "TGIF: The Evolution of Developer Commits Over Time"

This repository contains the replication package for the research paper **"TGIF: The Evolution of Developer Commits Over Time"**. Follow the steps outlined below to reproduce the results presented in the study.

## Table of Contents

1. [Collect Initial Projects](#collect-initial-projects)
2. [Sampling](#sampling)
3. [Data Cleaning & Writing Data to CSV Files](#data-cleaning--writing-data-to-csv-files)
    - [Data Cleaning](#data-cleaning)
    - [Assess Timezone Reliability](#assess-timezone-reliability)
    - [Write Data to CSV](#write-data-to-csv)
4. [Statistical Analysis & Plots](#statistical-analysis--plots)
5. [Distribution of Programming Languages](#distribution-of-programming-languages)
6. [Paid vs Volunteering Analysis](#paid-vs-volunteering-analysis)

---

## Collect Initial Projects

1. Visit the [SEART GitHub Search](https://seart-ghs.si.usi.ch/).
2. Apply the following filters:
   - **Number of Commits**: Minimum = 12,730
   - **Number of Stars**: Minimum = 10
   - **Number of Forks**: Minimum = 10
   - **Number of Contributors**: Minimum = 10
   - **Exclude Forks**
   - **Created no later than**: 12/31/2024
3. Download the search results as a CSV file.

## Sampling

1. Navigate to the `sampling` directory.
2. Run `extract_and_validate_repos.py` to extract repository names from the CSV file and validate they exist on GitHub.
3. Optionally run `repo_information_scraper.py` to gather additional repository information.
4. Fetch the projects by running `fetch-projects.sh`.

## Data Cleaning & Writing Data to CSV Files

### Data Cleaning

1. Return to the base directory and then navigate to the `data-cleaning/inactive-projects` directory.
2. Run `remove_inactive_repos.py` to identify and remove repositories with last commit before 2015 from results.json.

### Assess Timezone Reliability

1. Return to the base directory and then navigate to the `data-cleaning/timezone-reliability-assessment` directory.
2. Run `count_all_timezone_commits.bash` for every desired year to calculate all commits per timezone.
3. Run `analyze_timezone_per_repo.bash` to analyze timezone patterns per repository.
4. Run `calculate_utc_percentage.py` to calculate UTC+0000 commit percentages for specific years.
5. Run `analyze_filtered_timezone_commits.py` to count commits from contributors with timezone variation (filters out likely automated commits).
6. Run `calculate_yearly_timezone_variations.py` to calculate variation metrics including standard deviation, coefficient of variation, and entropy.

### Write Data to CSV

1. Return to the base directory and then navigate to the `write-data-in-csv` directory.
2. Generate commit counts and proportions per day by running `commit_count_per_day.py`.
3. Generate commit counts and proportions per hour by running `commit_count_per_hour.py`.

## Statistical Analysis & Plots

1. Return to the base directory and then navigate to the `statistical-analysis` directory.
2. For Mann-Kendall trend tests, navigate to `mann-kendall` and run the desired scripts.
3. For Kruskal-Wallis tests, navigate to `kruskal-wallis` and run `kruskal.py`.
4. For effect size calculations, navigate to `effect-sizes` and run the Cohen's h scripts.
5. For linear regression analysis, navigate to `linear-regression` and run the regression assumption scripts.
6. Return to the base directory and then navigate to the `plots` directory.
7. Run the desired plotting scripts such as `daily_stacked_bar_chart.py`, `hourly_frequencies.py`, `total_commits_per_period.py`, etc.


## Distribution of Programming Languages

To analyze the distribution of programming languages in the sampled projects:

1. Navigate to the `distribution-of-languages` directory.
2. Run `find_loc_and_occurrences.py` to count repositories and lines of code per programming language.
3. Run `find_last_commits_per_project.py` to analyze repository activity over time and generate active repos per year data.

## Paid vs Volunteering Analysis

To analyze differences between company-backed and volunteering projects:

1. Navigate to the `paid_vs_volunteering` directory.
2. Run `random_sample.py` to generate a random sample of repositories for manual classification.
3. Manually classify the repositories in `random_repos_sample.txt` as company or volunteering projects.

---
