# Plots

* [`daily_stacked_bar_chart.py`](daily_stacked_bar_chart.py) reads commit data from a CSV file and generates a stacked bar chart showing the number or proportion of commits for selected days of the week (e.g., Monday to Sunday) across different periods (e.g., years).  
  Run `python daily_stacked_bar_chart.py <filename.csv>`

* [`hourly_frequencies.py`](hourly_frequencies.py) generates a grouped bar chart to show the frequency of commits for each hour block within two specified time periods.  
  Run `python hourly_frequencies.py <filename.csv> <period_name1> <period_name2>`

* [`hourly_stacked_bar_chart.py`](hourly_stacked_bar_chart.py) reads a CSV file containing time series data for various periods and plots a 100% stacked bar chart to visualize the distribution of data across specified time blocks. The user is prompted to input multiple time blocks (start and end) for aggregation.  
  Run `python hourly_stacked_bar_chart.py <filename>`

* [`total_commits_per_period.py`](total_commits_per_period.py) generates a bar chart showing total commits per period by reading and processing commit data from a CSV file.  
  Run `python total_commits_per_period.py <filename.csv>`

* [`weekdays_to_weekends_ratio.py`](weekdays_to_weekends_ratio.py) calculates and plots the ratio of average weekday commits to average weekend day commits over the years.  
  Run `python weekdays_to_weekends_ratio.py <filename.csv>`
