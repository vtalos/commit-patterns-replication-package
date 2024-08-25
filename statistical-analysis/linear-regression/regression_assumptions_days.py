import csv
from itertools import tee
import numpy as np
import sys
import argparse
import statsmodels.api as sm
import matplotlib.pyplot as plt
import statsmodels.stats.api as sms
import scipy.stats as stats
import statsmodels.api as sm

parser = argparse.ArgumentParser(description="A script for checking if linear regression assumptions are meeted for a set of data")

parser.add_argument("filename", help="The csv file to get the data from")
parser.add_argument("day", help="The day of the week to implement the linear regression")

filename = sys.argv[1] # The first argument is the filename
week_day = sys.argv[2] # The second argument is the day of the week

day_total = []
all_commits = [[] for _ in range(7)]
sum_period = []

# Open the csv file and read its contents into the lists
with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    periods = next(reader)  # Skip header row
    # Copy the reader
    reader_copy1, reader_copy2 = tee(reader)
    num_of_periods = len(periods)
    period = [[] for _ in range(num_of_periods)]

    # Append the number of commits for each day in each period
    for row in reader_copy2:
        for i in range(1, len(period)):
            period[i].append(float(row[i]))
    # Append for each week day the number of commits for every period
    for i in range(len(period[1])):
        total_commits = 0
        for j in range(1, len(period)):
            all_commits[i].append(period[j][i]) # Calculate the total number of commits for each day
            total_commits += period[j][i]
        day_total.append(total_commits)
    # Calculate total commits for each period
    for i in range(1, len(period)):
        sum_period.append(sum(period[i]))

per = range(1, len(periods))
periods = periods[1:len(periods)]
data = all_commits[int(week_day)]
time_periods = range(1, len(periods) + 1)

# Perform ordinary least squares (OLS) regression
X = sm.add_constant(time_periods)  # Add a constant term (intercept) to the model
model = sm.OLS(data, X).fit()

# Check linearity with a scatter plot
plt.scatter(time_periods, data)
plt.xlabel("Time Periods")
plt.ylabel("Frequencies")
plt.title("Scatter Plot of Time Periods vs. Frequencies")
plt.show()

# Check Independence of Residuals with a Durbin-Watson test
durbin_watson_stat = sms.durbin_watson(model.resid)
print("Durbin-Watson statistic:", durbin_watson_stat)
# A value around 2 suggests no significant autocorrelation.

# Check Homoscedasticity with a plot of residuals vs. predicted values
predicted_values = model.predict(X)
residuals = model.resid
plt.scatter(predicted_values, residuals)
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residuals vs. Predicted Values")
plt.show()

# Check Normality of Residuals with a histogram
residuals = model.resid
plt.hist(residuals, bins=20)
plt.xlabel("Residuals")
plt.ylabel("Frequency")
plt.title("Histogram of Residuals")
plt.show()

# Check for normality using a Q-Q plot
residuals_standardized = (residuals - residuals.mean()) / residuals.std()
stats.probplot(residuals_standardized, dist="norm", plot=plt)
plt.title("Normal Q-Q Plot")
plt.show()
