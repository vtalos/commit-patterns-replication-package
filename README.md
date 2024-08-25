# Replication Package for "TGIF: The Evolution of Developer Work Times"

This repository contains the replication package for the research paper **"TGIF: The Evolution of Developer Work Times"**. Follow the steps outlined below to reproduce the results presented in the study.

## Table of Contents

1. [Collect Initial Projects](#collect-initial-projects)
2. [Sampling](#sampling)
3. [Data Cleaning & Writing Data to CSV Files](#data-cleaning--writing-data-to-csv-files)
    - [Data Cleaning](#data-cleaning)
    - [Writing Data to CSV](#writing-data-to-csv)
4. [Statistical Analysis & Plots](#statistical-analysis--plots)
5. [Discussion](#discussion)
   - [Work-Life Balance Analysis](#work-life-balance-analysis)
6. [Distribution of Programming Languages](#distribution-of-programming-languages)

---

## Collect Initial Projects

1. Visit the [SEART GitHub Search](https://seart-ghs.si.usi.ch/).
2. Apply the following filters:
   - **Number of Commits**: Minimum = 12,730
   - **Number of Stars**: Minimum = 10
   - **Number of Forks**: Minimum = 10
   - **Number of Contributors**: Minimum = 10
3. Download the search results as a CSV file.

## Sampling

1. Navigate to the `sampling` directory.
2. Run `repo_sampler.py` to sample the repositories.
3. Fetch the projects by running `fetch-projects.sh`.

## Data Cleaning & Writing Data to CSV Files

### Data Cleaning

1. Return to the base directory and then navigate to the `data-cleaning/find-duplicates` directory.
2. Run `find_duplicates.py` to identify duplicate projects.
3. Manually inspect the identified duplicates and remove one of each duplicate from the accepted projects text file.

> **TODO:** Add the steps for the `2013-spike-analysis` and `timezone-reliability-assessment` directories.

### Writing Data to CSV

1. Return to the base directory and then navigate to the `write-data-in-csv` directory.
2. Generate commit counts and proportions per day by running `commit_count_per_day.py`.
3. Generate commit counts and proportions per hour by running `commit_count_per_hour.py`.

## Statistical Analysis & Plots

1. Return to the base directory and then navigate to the `statistical-analysis` directory.
2. Run the desired scripts to perform the statistical analysis.
3. Return to the base directory and then navigate to the `plots` directory.
4. Run the desired scripts to generate the plots.

## Discussion

### Work-Life Balance Analysis

1. Visit [Scopus](https://www.scopus.com/).
2. Perform the first search:
    - **Search within:** language - **Search Documents:** English
    - Click **'Analyze results'**
    - Select year range to analyze: **2000 to 2023**
    - Click **'Export' -> 'Export the data to a CSV file'-> 'Export'**
3. Perform the second search:
    - **Search within:** `Article title, Abstract, Keywords` - **Search Documents:** `"wellness" OR "well-being" OR "work-life balance"`
      **and within:** language - **Search Documents:** English
    - Click **'Analyze results'**
    - Select year range to analyze: **2000 to 2023**
    - Click **'Export' -> 'Export the data to a CSV file'-> 'Export'**

4. In the `discussion/work-life-balance-approach` directory, run `publication-analysis.py`.

> **TODO:** Add the steps for the remaining directories in the `discussion` folder.

## Distribution of Programming Languages

To analyze the distribution of programming languages in the sampled projects:

1. Navigate to the `distribution-of-languages` directory.
2. Run `find_distribution.py` to find the distribution.

---
