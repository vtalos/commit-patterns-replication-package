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

filename = sys.argv[1] # The first argument is the file name
time_block = int(sys.argv[2]) # The second argument is the time block to keep for the linear regression assumptions check

hours = []

# Open the csv file and read its contents into the lists
with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    periods = next(reader)  # Skip header row
    # Copy the reader
    reader_copy1, reader_copy2, reader_copy3 = tee(reader, 3)
    num_of_periods = len(periods)
    period = [[] for _ in range(num_of_periods)]

    for row in reader_copy2:
        for i in range(1, len(period)):
            period[i].append(float(row[i]))

    # Split day in 1-hour blocks
    for row in reader_copy3:
        hours.append(row[0])

data = []

for per in period:
    if len(per) > 0:
        data.append(per[time_block])

p = range(len(periods) - 1)

# Perform ordinary least squares (OLS) regression
X = sm.add_constant(p)  # Add a constant term (intercept) to the model
model = sm.OLS(data, X).fit()

# Check linearity with a scatter plot
plt.scatter(p, data)
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

