# Linear Regression Assumptions Check

* [`regression_assumptions_days.py`](regression_assumptions_days.py) checks whether the assumptions of linear regression are met for a set of data based on the number of commits for a specified day of the week. The script performs an Ordinary Least Squares (OLS) regression and checks for linearity, independence of residuals, homoscedasticity, and normality of residuals.  
  Run `python regression_assumptions_days.py <filename.csv> <day>`

* [`regression_assumptions_hours.py`](regression_assumptions_hours.py) checks whether the assumptions of linear regression are met for a specific hourly time block of commit data. The script focuses on a specific hour, performs an Ordinary Least Squares (OLS) regression, and checks for linearity, independence of residuals, homoscedasticity, and normality of residuals.  
  Run `python regression_assumptions_hours.py <filename.csv> <time_block>`
