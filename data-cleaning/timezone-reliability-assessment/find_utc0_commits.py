from git import Repo
from collections import defaultdict
import os
import argparse

parser = argparse.ArgumentParser(description='Creates a CSV containing commit count per day of the week '
                                              'for a given interval and repository')
parser.add_argument('year', type=int, help='The year commit counting starts')
parser.add_argument('repos', type=str, help='The file containing repository names')
parser.add_argument('repos_path', type=str, help='The path for the directory that contains the cloned repos')
args = parser.parse_args()


# Read the file and split the lines to get repository names
with open(args.repos, 'r') as file:
    repo_list = [line.strip() for line in file.readlines()]

repos_path = args.repos_path
utc_0_commits = 0
non_utc0_commits = 0
for repository in repo_list:
    print(f"Processing repository: {repository}")
    repo_path = os.path.join(repos_path, repository)
    repo = Repo(repo_path)
    commits = repo.iter_commits(reverse=True, since=f"{args.year-1}-12-31", until=f"{args.year+1}-01-01")
    for commit in commits:
        contributor = commit.author.email
        year = commit.authored_datetime.year
        if year == args.year and commit.authored_datetime.strftime('%z') == "+0000":
            utc_0_commits += 1
        if year == args.year and commit.authored_datetime.strftime('%z') != "+0000":
            non_utc0_commits += 1
percentage = (utc_0_commits / (utc_0_commits + non_utc0_commits)) * 100 if (utc_0_commits + non_utc0_commits) > 0 else 0       
with open(f'commits_utc0_{args.year}.txt', 'w') as f:
    f.write(f"{args.year}: {percentage}")