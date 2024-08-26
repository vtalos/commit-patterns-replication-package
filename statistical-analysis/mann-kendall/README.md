# Mann-Kendall

* [`mann_kendall_days.py`](mann_kendall_days.py) performs the Mann-Kendall trend test on commit data from a CSV file, analyzing trends in the number of commits made on a specified day of the week over a series of time periods. It generates a plot showing the number of commits over time and highlights any significant trends detected.  
  Run `python mann_kendall_days.py <filename> <day_of_week>`

* [`mann_kendall_hours.py`](mann_kendall_hours.py) performs the Mann-Kendall trend test on time-blocked commit data from a CSV file, analyzing trends in the number of commits within a specified range of hours over a series of time periods. It generates a plot showing the number of commits over time and highlights any significant trends detected.  
  Run `python mann_kendall_hours.py <filename> <time_block_start> <time_block_end>`
