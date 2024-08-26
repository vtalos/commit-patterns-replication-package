# Work-Life Balance Approach

* [`publication_analysis.py`](publication_analysis.py) reads data from two CSV files, calculates the year-over-year percentage increase in publications for both total publications and work-life balance-related publications, and compares their average percentage increases. The script outputs the average percentage increase for each category and indicates which category has a larger average increase.  
  Run the script with `total_publications.csv` and `work_life_balance_publications.csv` in the same directory.

* [`total_publications.csv`](total_publications.csv) contains data on the total number of publications per year. Each row represents a year, and the corresponding number of publications is provided in the second column. This file is used by `publication_analysis.py` to calculate the percentage increase in total publications year-over-year.

* [`work_life_balance_publications.csv`](work_life_balance_publications.csv) contains data on the number of work-life balance-related publications per year. Each row represents a year, and the corresponding number of publications is provided in the second column. This file is used by `publication_analysis.py` to calculate the percentage increase in work-life balance-related publications year-over-year.
