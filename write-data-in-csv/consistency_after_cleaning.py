"""
Check if repositories meet commit consistency criteria over 6-month intervals.
Excludes contributors who have only UTC+0 commits and checks if each 6-month interval 
from 2004-2023 has sufficient commits.

Usage:
    python consistency_after_cleaning.py <repos_file> <repos_path>
"""

from collections import defaultdict
from git import Repo
from datetime import datetime, timedelta
import argparse
import os

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Check repositories for commit consistency over 6-month intervals')
    parser.add_argument('repos_file', type=str, help='File containing repository names')
    parser.add_argument('repos_path', type=str, help='Path to directory containing cloned repos')
    return parser.parse_args()

def read_repo_list(repo_file):
    """Read repository names from file."""
    with open(repo_file, 'r') as file:
        return [line.strip() for line in file.readlines()]

def get_six_month_intervals():
    """Generate 40 six-month intervals from 2004 to 2023."""
    intervals = []
    start_date = datetime(2004, 1, 1)
    
    for i in range(40):
        interval_start = datetime(start_date.year + (start_date.month + 6*i - 1) // 12,
                                ((start_date.month + 6*i - 1) % 12) + 1, 1)
        
        # Calculate end date (start of next interval minus 1 day)
        next_interval = datetime(start_date.year + (start_date.month + 6*(i+1) - 1) // 12,
                               ((start_date.month + 6*(i+1) - 1) % 12) + 1, 1)
        interval_end = next_interval - timedelta(days=1)
        
        intervals.append((interval_start, interval_end))
    
    return intervals

def count_commits_per_interval(repo_path):
    """
    Count commits per 6-month interval, following the original UTC+0 logic:
    - Track when each contributor makes their first non-UTC+0 commit
    - Only count commits from that point forward for each contributor
    
    Returns:
        tuple: (total_valid_commits, commits_per_interval_list)
    """
    repo = Repo(repo_path)
    intervals = get_six_month_intervals()
    
    # Get all commits sorted by date (oldest first)
    all_commits = list(repo.iter_commits())
    all_commits.reverse()  # Now oldest first
    
    # Track when each contributor first makes a non-UTC+0 commit
    contributor_activation = {}  # email -> datetime when they first made non-UTC+0 commit
    commits_per_interval = [0] * 40
    total_valid_commits = 0
    
    for commit in all_commits:
        contributor = commit.author.email
        commit_datetime = commit.authored_datetime.replace(tzinfo=None)
        
        # Check if this is a non-UTC+0 commit and contributor hasn't been activated yet
        if (commit.authored_datetime.strftime('%z') != "+0000" and 
            contributor not in contributor_activation):
            contributor_activation[contributor] = commit_datetime
        
        # Count this commit if the contributor has been activated and 
        # this commit is at or after their activation time
        if (contributor in contributor_activation and 
            commit_datetime >= contributor_activation[contributor]):
            
            # Find which interval this commit belongs to
            for i, (start_date, end_date) in enumerate(intervals):
                if start_date <= commit_datetime <= end_date:
                    commits_per_interval[i] += 1
                    total_valid_commits += 1
                    break
    
    return total_valid_commits, commits_per_interval

def check_repository_criteria(repo_name, repo_path):
    """
    Check if repository meets the commit consistency criteria.
    
    Returns:
        bool: True if repository meets criteria, False otherwise
    """
    print(f"Processing repository: {repo_name}")
    
    try:
        total_commits, commits_per_interval = count_commits_per_interval(repo_path)
        
        if total_commits == 0:
            print(f"  No valid commits found (all contributors UTC+0 only)")
            return False
        
        # Calculate threshold: total_commits / 40 / 5
        threshold = round(total_commits / 40 / 5)
        print(f"  Total valid commits: {total_commits}, Threshold per interval: {threshold}")
        
        # Check each 6-month interval
        for i, commit_count in enumerate(commits_per_interval):
            interval_start, interval_end = get_six_month_intervals()[i]
            print(f"  Interval {i+1} ({interval_start.strftime('%Y-%m')} to {interval_end.strftime('%Y-%m')}): {commit_count} commits")
            
            if commit_count < threshold:
                print(f"Failed at interval {i+1}: {commit_count} < {threshold}")
                return False
        
        print(f"Repository meets criteria!")
        return True
        
    except Exception as e:
        print(f"  Error processing repository: {e}")
        return False

def main():
    """Main function."""
    args = parse_arguments()
    repo_list = read_repo_list(args.repos_file)
    
    print(f"Checking {len(repo_list)} repositories for commit consistency...")
    print("Criteria: Each 6-month interval (2004-2023) must have >= (total_commits/40/5) commits")
    print("Note: Only counting commits from contributors with at least one non-UTC+0 commit\n")
    
    qualifying_repos = []
    
    for repo_name in repo_list:
        repo_path = os.path.join(args.repos_path, repo_name)
        
        if not os.path.exists(repo_path):
            print(f"Repository path not found: {repo_path}")
            continue
            
        if check_repository_criteria(repo_name, repo_path):
            qualifying_repos.append(repo_name)
        
        print()  # Empty line for readability
    
    # Output results
    print("=" * 60)
    print(f"RESULTS: {len(qualifying_repos)} out of {len(repo_list)} repositories meet the criteria:")
    print("=" * 60)
    
    if qualifying_repos:
        for repo in qualifying_repos:
            print(f"{repo}")
    else:
        print("No repositories meet the criteria.")
    
    # Save results to file
    with open('qualifying_repositories.txt', 'w') as f:
        for repo in qualifying_repos:
            f.write(f"{repo}\n")
    
    print(f"\nQualifying repositories saved to 'qualifying_repositories.txt'")

if __name__ == "__main__":
    main()