import pandas as pd

# Read the CSV file containing the repository data
df = pd.read_csv('ghs_results.csv')

df['name'].to_csv('projects-accepted.txt', index=False, header=False)
