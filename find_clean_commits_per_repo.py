from git import Repo
from collections import defaultdict
import os
import argparse

parser = argparse.ArgumentParser(description='Creates a CSV containing commit count per day of the week '
                                              'for a given interval and repository')
parser.add_argument('repos', type=str, help='The file containing repository names')
parser.add_argument('repos_path', type=str, help='The path for the directory that contains the cloned repos')
args = parser.parse_args()

OUTPUT_DIR = "commits_per_timezone"

# Read the file and split the lines to get repository names
with open(args.repos, 'r') as file:
    repo_list = [line.strip() for line in file.readlines()]

repos_path = args.repos_path
most_common_timezone = defaultdict(int)
for repository in repo_list:
    timezone_commits = defaultdict(int)
    non_utc0_commits = defaultdict(bool)
    print(f"Processing repository: {repository}")
    repo_path = os.path.join(repos_path, repository)
    repo = Repo(repo_path)
    for commit in repo.iter_commits():
        contributor = commit.author.email
        timezone = commit.authored_datetime.strftime('%z')
        print(commit.authored_datetime.tzinfo.dst(), timezone)
        if timezone != "+0000":
            non_utc0_commits[contributor] = True
        
        if non_utc0_commits[contributor]:
            timezone_commits[timezone] += 1
    # find the timezone with the most commits
    print(f"Timezone commits for {repository}: {timezone_commits}")
    if timezone_commits:
        most_commits_tz = max(timezone_commits, key=timezone_commits.get) 
        print(f"Most common timezone for {repository}: {most_commits_tz} with {timezone_commits[most_commits_tz]} commits")
        most_common_timezone[most_commits_tz] += 1
    with open(f"{OUTPUT_DIR}/{repository.replace('/','-')}_commits_per_timezone.txt", 'w') as f:
        for tz, count in timezone_commits.items():
            f.write(f"{tz},{count}\n")
with open("most_common_timezone.txt", 'w') as f:
    for tz, count in most_common_timezone.items():
        f.write(f"{tz},{count}\n")
