from collections import defaultdict
from git import Repo
import argparse
import statistics

parser = argparse.ArgumentParser(description='Calculates the coefficient of variation of accepted commits per year per timezone')
parser.add_argument('repos_path', type=str, help='The path for the file that contains the cloned repo')
parser.add_argument('start_year', type=int, help='The year commit counting starts')
parser.add_argument('end_year', type=int, help='The year commit counting stops')
args = parser.parse_args()


non_utc0_commits = defaultdict(bool)
repo_path = args.repos_path
repo = Repo(repo_path)
commits_by_year_timezones = defaultdict(lambda: defaultdict(int))

for commit in repo.iter_commits():
    contributor = commit.author.email
    if commit.authored_datetime.strftime('%z') != "+0000":
        non_utc0_commits[contributor] = True
    if non_utc0_commits[contributor] == True:
        year = commit.authored_datetime.year
        if args.start_year <= year <= args.end_year:
            timezone = commit.authored_datetime.strftime('%z')
            if timezone != "+0000": #exclude UTC-0
                commits_by_year_timezones[year][timezone] += 1
for year, timezones in sorted(commits_by_year_timezones.items()):
        print(year, max(timezones, key=timezones.get))
                
