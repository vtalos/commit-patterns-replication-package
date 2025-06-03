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

with open(args.repos, 'r') as file:
    repo_list = [line.strip() for line in file.readlines()]

repos_path = args.repos_path
most_common_timezone = defaultdict(int)
if args.compare:
    most_common_timezone2004 = defaultdict(int)
    most_common_timezone2023 = defaultdict(int)

for repository in repo_list:
    timezone_commits = defaultdict(int)
    if args.compare:
        timezone_commits2004 = defaultdict(int)
        timezone_commits_2023 = defaultdict(int)
    print(f"Processing repository: {repository}")
    repo_path = os.path.join(repos_path, repository)
    repo = Repo(repo_path)
    commits = list(repo.iter_commits())

    # --- Begin contributor best offset detection ---
    contributor_timezones = defaultdict(list)
    for commit in commits:
        contributor = commit.author.email
        offset_str = commit.authored_datetime.strftime('%z')
        contributor_timezones[contributor].append((commit.authored_datetime, offset_str))

    contributor_best_timezone = {}
    for contributor, commit_data in contributor_timezones.items():
        # Find the oldest non-UTC timezone for this contributor
        non_utc_offsets = [(dt, offset) for dt, offset in commit_data if offset != "+0000"]
        if non_utc_offsets:
            non_utc_offsets.sort(key=lambda x: x[0])
            best_offset = non_utc_offsets[0][1]
            contributor_best_timezone[contributor] = best_offset
    # --- End contributor best offset detection ---

    if not args.compare:
        for commit in commits:
            contributor = commit.author.email
            offset_str = commit.authored_datetime.strftime('%z')
            year = commit.authored_datetime.year
            if contributor in contributor_best_timezone:
                if offset_str == "+0000":
                    tz = contributor_best_timezone[contributor]
                else:
                    tz = offset_str
            else:
                tz = offset_str  # fallback (could be only UTC)
            if year >= 2004 and year <= 2023:
                timezone_commits[tz] += 1
    if args.compare:
        for commit in commits:
            contributor = commit.author.email
            offset_str = commit.authored_datetime.strftime('%z')
            year = commit.authored_datetime.year
            if contributor in contributor_best_timezone:
                if offset_str == "+0000":
                    tz = contributor_best_timezone[contributor]
                else:
                    tz = offset_str
            else:
                tz = offset_str
            if year == 2004:
                timezone_commits2004[tz] += 1
            if year == 2023:
                timezone_commits_2023[tz] += 1

    # find the timezone with the most commits
    os.makedirs(OUTPUT_DIR, exist_ok=True)
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