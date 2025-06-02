from git import Repo
from collections import defaultdict
import os
import argparse

parser = argparse.ArgumentParser(description='Creates a CSV containing commit count per day of the week '
                                              'for a given interval and repository')
parser.add_argument('repos', type=str, help='The file containing repository names')
parser.add_argument('repos_path', type=str, help='The path for the directory that contains the cloned repos')
parser.add_argument('--compare', action="store_true", help='If set, creates  timezone allocation of commits for 2004 and 2023')
args = parser.parse_args()

OUTPUT_DIR = "commits_per_timezone"

# Read the file and split the lines to get repository names
with open(args.repos, 'r') as file:
    repo_list = [line.strip() for line in file.readlines()]

repos_path = args.repos_path
most_common_timezone = defaultdict(int)
for repository in repo_list:
    timezone_commits = defaultdict(int)
    if args.compare:
        timezone_commits2004 = defaultdict(int)
        timezone_commits_2023 = defaultdict(int)
        most_common_timezone2004 = defaultdict(int)
        most_common_timezone2023 = defaultdict(int)
    non_utc0_commits = defaultdict(bool)
    print(f"Processing repository: {repository}")
    repo_path = os.path.join(repos_path, repository)
    repo = Repo(repo_path)
    commits = reversed(list(repo.iter_commits()))
    if not args.compare:
        for commit in commits:
            contributor = commit.author.email
            timezone = commit.authored_datetime.strftime('%z')
            year = commit.authored_datetime.year
            if timezone != "+0000":
                non_utc0_commits[contributor] = True
            if non_utc0_commits[contributor]:
                timezone_commits[timezone] += 1
    if args.compare:
        for commit in commits:
            contributor = commit.author.email
            timezone = commit.authored_datetime.strftime('%z')
            year = commit.authored_datetime.year
            if timezone != "+0000":
                non_utc0_commits[contributor] = True     
            if year == 2004 and non_utc0_commits[contributor]:
                timezone_commits2004[timezone] += 1
            if year == 2023 and non_utc0_commits[contributor]:
                timezone_commits_2023[timezone] += 1

    # find the timezone with the most commits
    
    if not args.compare:
        if timezone_commits:
            most_commits_tz = max(timezone_commits, key=timezone_commits.get)
            print(f"Most common timezone for {repository}: {most_commits_tz} with {timezone_commits[most_commits_tz]} commits")
            most_common_timezone[most_commits_tz] += 1
            with open(f"{OUTPUT_DIR}/{repository.replace('/','-')}_commits_per_timezone.txt", 'w') as f:
                for tz, count in timezone_commits.items():
                    f.write(f"{tz},{count}\n")
    if args.compare:
        if timezone_commits2004:
            most_commits_tz2004 = max(timezone_commits2004, key=timezone_commits2004.get, default=None)
            most_common_timezone2004[most_commits_tz2004] += 1
            with open(f"{OUTPUT_DIR}/{repository.replace('/','-')}_commits_per_timezone_2004.txt", 'w') as f:
                for tz, count in timezone_commits2004.items():
                    f.write(f"{tz},{count}\n")
        if timezone_commits_2023:
            most_commits_tz2023 = max(timezone_commits_2023, key=timezone_commits_2023.get, default=None) 
            most_common_timezone2023[most_commits_tz2023] += 1
            with open(f"{OUTPUT_DIR}/{repository.replace('/','-')}_commits_per_timezone_2023.txt", 'w') as f:
                for tz, count in timezone_commits_2023.items():
                    f.write(f"{tz},{count}\n")
if not args.compare:
    with open("most_common_timezone.txt", 'w') as f:
        for tz, count in most_common_timezone.items():
            f.write(f"{tz},{count}\n")
if args.compare:
    with open("most_common_timezone_2004.txt", 'w') as f:
        for tz, count in most_common_timezone2004.items():
            f.write(f"{tz},{count}\n")
    with open("most_common_timezone_2023.txt", 'w') as f:
        for tz, count in most_common_timezone2023.items():
            f.write(f"{tz},{count}\n")
