"""
This script counts the number of commits made on each day of the week over specified time intervals for a set of Git repositories. 
It can either output the total commit counts or the proportion of commits per day relative to the total commits in the interval.
The script now also produces separate files for each repository in addition to the combined results.

Usage:
    python commit_count_per_day.py <start_year> <end_year> <interval> <contents> <repos> <repos_path>
"""
from collections import defaultdict
from git import Repo
import argparse
import csv
import os
from datetime import datetime, timezone, timedelta

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
    parser.add_argument('repos', type=str, help='File containing repository names')
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

def parse_timezone_offset(offset_str):
    """
    Parse timezone offset string (+HHMM or -HHMM) and return a timezone object.
    
    Args:
        offset_str (str): Timezone offset string like '+0200' or '-0500'
    
    Returns:
        timezone: Python timezone object
    """
    if not offset_str or len(offset_str) != 5:
        return timezone.utc
    
    try:
        sign = 1 if offset_str[0] == '+' else -1
        hours = int(offset_str[1:3])
        minutes = int(offset_str[3:5])
        total_minutes = sign * (hours * 60 + minutes)
        return timezone(timedelta(minutes=total_minutes))
    except (ValueError, IndexError):
        return timezone.utc

def count_commits(repo_list, repos_path, start_year, interval, num_of_periods):
    """
    Count the number of commits per day of the week for each repository.
    Now uses retroactive timezone correction for contributors.

    Args:
        repo_list (list): A list of repository names.
        repos_path (str): The path to the directory containing the repositories.
        start_year (int): The starting year for the commit counting.
        interval (int): The number of years in each interval.
        num_of_periods (int): The total number of periods calculated.

    Returns:
        tuple: A tuple containing:
            - defaultdict: Combined commit counts for all repositories
            - dict: Individual commit counts for each repository
    """
    combined_commit_counts = defaultdict(lambda: [0] * num_of_periods)
    individual_commit_counts = {}
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for repository in repo_list:
        repo_commit_counts = defaultdict(lambda: [0] * num_of_periods)
        print(f"Processing repository: {repository}")
        repo_path = os.path.join(repos_path, repository)
        repo = Repo(repo_path)

        # First pass: collect contributor timezone information
        contributor_timezones = defaultdict(list)
        all_commits = list(repo.iter_commits())
        
        for commit in all_commits:
            contributor = commit.author.email
            offset_str = commit.authored_datetime.strftime('%z')
            contributor_timezones[contributor].append((commit.authored_datetime, offset_str))
        
        # Determine the best timezone for each contributor
        contributor_best_timezone = {}
        for contributor, commit_data in contributor_timezones.items():
            # Find the oldest non-UTC timezone for this contributor
            non_utc_offsets = [(dt, offset) for dt, offset in commit_data if offset != "+0000"]
            
            if non_utc_offsets:
                # Use the oldest non-UTC timezone (earliest chronologically)
                non_utc_offsets.sort(key=lambda x: x[0])  # Sort by datetime, earliest first
                best_offset = non_utc_offsets[0][1]
                contributor_best_timezone[contributor] = parse_timezone_offset(best_offset)
        
        # Second pass: count commits using corrected timezones
        print(f"  Second pass: counting commits with timezone corrections...")
        
        for commit in reversed(all_commits):
            contributor = commit.author.email
            # If the contributor has only UTC +0 commits he is not in the keys of contributor_timezones
            if contributor in contributor_best_timezone:
                
                best_timezone = contributor_best_timezone[contributor]

                # Get the original UTC datetime
                original_datetime = commit.authored_datetime.replace(tzinfo=timezone.utc)

                # Convert to the contributor's best known timezone
                corrected_datetime = original_datetime.astimezone(best_timezone)

                # Get the day of week from the corrected time
                day_index = corrected_datetime.weekday()
                interval_index = (corrected_datetime.year - start_year) // interval

                if 0 <= interval_index < num_of_periods:
                    # Add to both combined and individual counts
                    combined_commit_counts[day_index][interval_index] += 1
                    repo_commit_counts[day_index][interval_index] += 1

        individual_commit_counts[repository] = repo_commit_counts
        print(f"  Completed processing {repository}")

    return combined_commit_counts, individual_commit_counts

def write_counts(args, commit_counts, days_of_week, filename_prefix="CommitCountsPerDay"):
    """
    Write commit counts to a CSV file.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        commit_counts (dict): The dictionary with commit counts.
        days_of_week (list): The list of days in the week.
        filename_prefix (str): Prefix for the output filename.
    
    Returns:
        str: The filename that was written to.
    """
    filename = f'{filename_prefix}.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header_row = generate_header_row(args.start_year, args.end_year, args.interval)
        writer.writerow(header_row)

        for day_index, day in enumerate(days_of_week):
            writer.writerow([day] + [str(count) for count in commit_counts[day_index]])
    print(f"Commit counts written to {filename}")
    return filename

def write_proportions(args, commit_counts, days_of_week, num_of_periods, filename_prefix="CommitPercentagesPerDay"):
    """
    Write commit proportions to a CSV file.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        commit_counts (dict): The dictionary with commit counts.
        days_of_week (list): The list of days in the week.
        num_of_periods (int): The total number of periods calculated.
        filename_prefix (str): Prefix for the output filename.
    
    Returns:
        str: The filename that was written to.
    """
    filename = f'{filename_prefix}.csv'
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
    return filename

def write_individual_repo_files(args, individual_commit_counts, days_of_week, num_of_periods):
    """
    Write separate CSV files for each repository.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        individual_commit_counts (dict): Dictionary with commit counts for each repository.
        days_of_week (list): The list of days in the week.
        num_of_periods (int): The total number of periods calculated.
    """
    # Create a directory for individual repository files
    output_dir = "individual_repos"
    os.makedirs(output_dir, exist_ok=True)
    
    for repo_name, commit_counts in individual_commit_counts.items():
        # Sanitize repository name for filename
        safe_repo_name = "".join(c for c in repo_name if c.isalnum() or c in ('-', '_')).rstrip()
        
        if args.contents == 'proportions':
            filename_prefix = os.path.join(output_dir, f"{safe_repo_name}_CommitPercentagesPerDay")
            write_proportions(args, commit_counts, days_of_week, num_of_periods, filename_prefix)
        else:
            filename_prefix = os.path.join(output_dir, f"{safe_repo_name}_CommitCountsPerDay")
            write_counts(args, commit_counts, days_of_week, filename_prefix)

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
    
    # Get both combined and individual commit counts
    combined_commit_counts, individual_commit_counts = count_commits(
        repo_list, args.repos_path, args.start_year, args.interval, num_of_periods
    )

    # Write combined results (original functionality)
    if args.contents == 'proportions':
        write_proportions(args, combined_commit_counts, days_of_week, num_of_periods)
    else:
        write_counts(args, combined_commit_counts, days_of_week)

    # Write individual repository files
    print(f"\nWriting individual repository files...")
    write_individual_repo_files(args, individual_commit_counts, days_of_week, num_of_periods)
    print(f"Individual repository files written to 'individual_repos/' directory")

if __name__ == "__main__":
    main()
