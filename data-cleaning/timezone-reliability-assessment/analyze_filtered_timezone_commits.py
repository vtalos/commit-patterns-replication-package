from git import Repo
from collections import defaultdict
import os
import argparse

parser = argparse.ArgumentParser(description='Creates a CSV containing commit count per day of the week '
                                              'for a given interval and repository')
parser.add_argument('start_year', type=int, help='The year commit counting starts')
parser.add_argument('end_year', type=int, help='The year commit counting stops')
parser.add_argument('repos', type=str, help='The file containing repository names')
parser.add_argument('repos_path', type=str, help='The path for the directory that contains the cloned repos')
args = parser.parse_args()


# Read the file and split the lines to get repository names
with open(args.repos, 'r') as file:
    repo_list = [line.strip() for line in file.readlines()]

repos_path = args.repos_path
commits_per_timezone = defaultdict(int)
for repository in repo_list:
    print(f"Processing repository: {repository}")
    non_utc0_commits = defaultdict(bool)
    repo_path = os.path.join(repos_path, repository)
    repo = Repo(repo_path)
    commits = repo.iter_commits(reverse=True, since=f"{args.start_year}-01-01", until=f"{args.end_year}-12-31")
    for commit in commits:
        contributor = commit.author.email
        if commit.authored_datetime.strftime('%z') != "+0000":
            non_utc0_commits[contributor] = True

        if non_utc0_commits[contributor]:
            timezone = commit.authored_datetime.strftime('%z')
            commits_per_timezone[timezone] += 1
with open('commits_per_timezone.txt', 'w') as f:
    for timezone, count in commits_per_timezone.items():
        f.write(f"{timezone},{count}\n")
