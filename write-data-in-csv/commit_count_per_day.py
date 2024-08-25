from collections import defaultdict
from git import Repo
import argparse
import csv
import os

def parse_arguments():
    """
    Parse and validate command-line arguments.

    Returns:
        args (argparse.Namespace): Parsed arguments containing start_year, end_year,
        interval, contents, repos, and repos_path.
    """
    parser = argparse.ArgumentParser(description='Creates a CSV containing commit count per day of the week '
                                                 'for a given interval and repository')
    parser.add_argument('start_year', type=int, help='The year commit counting starts')
    parser.add_argument('end_year', type=int, help='The year commit counting stops')
    parser.add_argument('interval', type=int, help='How many years a single interval contains')
    parser.add_argument('contents', type=str, choices=["proportions", "total"],
                        help='The contents of the CSV (proportions or total)')
    parser.add_argument('repos', type=str, help='Directory containing repository names')
    parser.add_argument('repos_path', type=str, help='The path for the file that contains the cloned repos')
    args = parser.parse_args()

    # Handle invalid arguments for start and end year
    if args.start_year > args.end_year:
        parser.error("Invalid arguments: start_year must be before end_year")

    # Handle invalid argument for interval
    if args.interval <= 0:
        parser.error("Invalid argument: interval must be a positive integer")

    return args

def read_repo_list(repo_file):
    """
    Read repository names from a file.

    Args:
        repo_file (str): The file containing repository names.

    Returns:
        list: A list of repository names.
    """
    with open(repo_file, 'r') as file:
        return [line.strip() for line in file.readlines()]

def count_commits(repo_list, repos_path, start_year, interval, num_of_periods):
    """
    Count the number of commits per day of the week for each repository.

    Args:
        repo_list (list): A list of repository names.
        repos_path (str): The path to the directory containing the repositories.
        start_year (int): The starting year for the commit counting.
        interval (int): The number of years in each interval.
        num_of_periods (int): The total number of periods calculated.

    Returns:
        defaultdict: A dictionary with commit counts for each day and period.
    """
    commit_counts = defaultdict(lambda: [0] * num_of_periods)
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for repository in repo_list:
        non_utc0_commits = defaultdict(bool)
        print(f"Processing repository: {repository}")
        repo_path = os.path.join(repos_path, repository)
        repo = Repo(repo_path)

        for commit in repo.iter_commits():
            contributor = commit.author.email
            if commit.authored_datetime.strftime('%z') != "+0000":
                non_utc0_commits[contributor] = True

            if non_utc0_commits[contributor]:
                day_index = commit.authored_datetime.weekday()
                interval_index = (commit.authored_datetime.year - start_year) // interval
                if 0 <= interval_index < num_of_periods:
                    commit_counts[day_index][interval_index] += 1

    return commit_counts

def write_counts(args, commit_counts, days_of_week):
    """
    Write commit counts to a CSV file.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        commit_counts (dict): The dictionary with commit counts.
        days_of_week (list): The list of days in the week.
    """
    filename = 'CommitCountsPerDay.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header_row = generate_header_row(args.start_year, args.end_year, args.interval)
        writer.writerow(header_row)

        for day_index, day in enumerate(days_of_week):
            writer.writerow([day] + [str(count) for count in commit_counts[day_index]])
    print(f"Commit counts written to {filename}")

def write_proportions(args, commit_counts, days_of_week, num_of_periods):
    """
    Write commit proportions to a CSV file.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        commit_counts (dict): The dictionary with commit counts.
        days_of_week (list): The list of days in the week.
        num_of_periods (int): The total number of periods calculated.
    """
    filename = 'CommitPercentagesPerDay.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header_row = generate_header_row(args.start_year, args.end_year, args.interval)
        writer.writerow(header_row)

        for day_index, day in enumerate(days_of_week):
            percentages = []
            for interval in range(num_of_periods):
                total_commits_interval = sum(commit_counts[other_day][interval] for other_day in range(len(days_of_week)))
                percentage = (commit_counts[day_index][interval] / total_commits_interval * 100 
                              if total_commits_interval != 0 else 0)
                percentages.append(percentage)
            writer.writerow([day] + percentages)
    print(f"Commit proportions written to {filename}")

def generate_header_row(start_year, end_year, interval):
    """
    Generate the header row for the CSV file.

    Args:
        start_year (int): The starting year for the commit counting.
        end_year (int): The ending year for the commit counting.
        interval (int): The number of years in each interval.

    Returns:
        list: The header row for the CSV file.
    """
    if interval == 1:
        return ['Day'] + [str(year) for year in range(start_year, end_year + 1)]
    else:
        return ['Day'] + [f'{year}-{year + interval - 1}' for year in range(start_year, end_year + 1, interval)]

def main():
    """
    Main function that orchestrates the execution of the script.
    """
    args = parse_arguments()
    repo_list = read_repo_list(args.repos)
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    num_of_periods = (args.end_year - args.start_year + 1) // args.interval
    commit_counts = count_commits(repo_list, args.repos_path, args.start_year, args.interval, num_of_periods)

    if args.contents == 'proportions':
        write_proportions(args, commit_counts, days_of_week, num_of_periods)
    else:
        write_counts(args, commit_counts, days_of_week)

if __name__ == "__main__":
    main()