"""
This script analyzes commit data stored in text files within a specified directory.

It expects each text file in the directory to follow a specific format:

- The first line contains the year (integer) as a string.
- Subsequent lines contain timezone data, where each line is formatted as
  'timezone: count'. 'timezone' is a string representing the timezone offset
  (e.g., '+0000' for UTC), and 'count' is an integer representing the number
  of commits for that timezone.

The script processes each file, calculates various statistics to analyze
the distribution of commits across timezones:

- Standard deviation (std dev): Measures the spread of commit counts from
  the average. A lower std dev indicates a more even distribution.
- Coefficient of variation (CV): A normalized version of std dev, dividing it
  by the mean. A lower CV provides a better relative measure of spread,
  making it less susceptible to the influence of overall commit volume.
- Entropy: Measures the uncertainty associated with the distribution of commits.
  A lower entropy suggests a more concentrated distribution.
- Percentage of UTC+0000 commits: The percentage of commits made in the UTC+0000
  timezone.

Finally, it prints and saves the year-wise statistics sorted by year.
"""
import os
import numpy as np
from scipy.stats import entropy

def read_commit_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        year = int(lines[0].strip())
        timezone_data = {}
        for line in lines[1:]:
            timezone, count = line.strip().split(': ')
            timezone_data[timezone] = int(count)
        return year, timezone_data

def calculate_standard_deviation(timezone_data):
    counts = list(timezone_data.values())
    return np.std(counts)

def calculate_coefficient_of_variation(timezone_data):
    counts = list(timezone_data.values())
    mean = np.mean(counts)
    std_dev = np.std(counts)
    return std_dev / mean if mean else 0

def calculate_entropy(timezone_data):
    counts = list(timezone_data.values())
    total_commits = sum(counts)
    probabilities = [count / total_commits for count in counts if total_commits > 0]
    return entropy(probabilities)

def calculate_percentage_utc(timezone_data):
    total_commits = sum(timezone_data.values())
    commits_utc = timezone_data.get('+0000', 0)
    return (commits_utc / total_commits) * 100 if total_commits > 0 else 0

def main(directory_path):
    year_stats = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            year, timezone_data = read_commit_data(file_path)
            std_dev = calculate_standard_deviation(timezone_data)
            cv = calculate_coefficient_of_variation(timezone_data)
            ent = calculate_entropy(timezone_data)
            percentage_utc = calculate_percentage_utc(timezone_data)
            year_stats.append((year, std_dev, cv, ent, percentage_utc))

    # Sort by year
    year_stats.sort()

    # Print and save results
    results = []
    for year, std_dev, cv, ent, percentage_utc in year_stats:
        result = f"{year}: Std Dev = {std_dev:.2f}, CV = {cv:.2f}, Entropy = {ent:.2f}, UTC+0000 = {percentage_utc:.2f}%"
        print(result)
        results.append(result)
    
    # Save to file
    with open(os.path.join(directory_path, "commit_variation_stats.txt"), 'w') as f:
        for result in results:
            f.write(result + "\n")

if __name__ == "__main__":
    main("commits-data")