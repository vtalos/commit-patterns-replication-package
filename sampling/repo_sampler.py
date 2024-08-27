"""
Repo Sampler

This script is part of a research study in the field of Mining Software Repositories (MSR). 
The study aims to examine developer work pattern changes during the decades by analyzing repositories hosted on GitHub.

The script takes a CSV file generated from the GitHub Search mining tool as input. 

Repositories contained in the CSV file have:
- At least 10 stars
- At least 10 forks
- At least 12730 commits

For each repository, it checks if it has a sufficient number of commits in 6-month intervals over a 20-year period. If a repository meets all criteria, it is written to a file named "projects-accepted.txt".

The script utilizes the GitHub API to fetch commit information and respects rate limits by handling rate limit exceeded errors.

Usage:
    python ghs_repo_sampler.py <file_input> <gh_token>

Arguments:
    file_input (str): The path to the CSV file generated from the GitHub Search mining tool.
    gh_token (str): GitHub personal access token for authentication of API calls.

Example:
    python ghs_repo_sampler.py ghs_results.csv <github_token>
"""
import csv
import requests
import time
import argparse
from dateutil.relativedelta import relativedelta
import datetime

parser = argparse.ArgumentParser(description='Given the CSV from GHS, returns the repos '
                                            'that fit all the requirements for the samping')
parser.add_argument('file_input', type=str, help='The CSV from GHS with at least 10 starts, 10 forks and 12730 commits', default='data/ghs_results.csv')
parser.add_argument('gh_token', type=str, help='GitHub token for authentication of calls')
args = parser.parse_args()

auth_token = args.gh_token

def handle_api(resp, url, headers):
    """
    Handles API response. If status code is 403 (rate limit exceeded),
    it waits for a minute and retries. If status code is not 200,
    retries up to 7 times.
    
    Args:
        resp (requests.Response): The response object.
        url (str): The URL for the request.
        headers (dict): The headers for the request.
    
    Returns:
        requests.Response or None: New response object if status is 200,
        None otherwise.
    """
    NUM_OF_TRIES = 7
    if resp.status_code == 403:
        # Handle rate limit exceeded error
        print(f"Rate limit exceeded. Wait 1 minute")
        time.sleep(60)
        new_resp = requests.get(url, headers=headers)
    else :
        j = 0
        while j < NUM_OF_TRIES and resp.status_code != 200:
            time.sleep(2)  # Wait for the process of the request
            new_resp = requests.get(url, headers=headers)
            j += 1
    if resp.status_code != 200:
        print(f'Skipping repository due to invalid gitHub response: {resp.content}')
        return None
    return new_resp

def search_commits_for_six_months_interval(owner, repo, commits):
    """
    Searches for commits in a 6 months interval for 20 years for a repository.
    
    Args:
        owner (str): Owner of the repository.
        repo (str): Name of the repository.
        commits (int): Number of commits in the repository.
    
    Returns:
        bool: True if repository meets the criteria, False otherwise.
    """
    threshold = round(int(commits) / 40 / 5)  
    for start in range(40):
        start_date = (datetime.datetime(2004, 1, 1) + relativedelta(months=6 * start)).strftime('%Y-%m-%d')
        end_date = (datetime.datetime(2004, 1, 1) + relativedelta(months=6 * (start + 1))).strftime('%Y-%m-%d')
        url = f"https://api.github.com/search/commits?q=repo:{owner}/{repo}+author-date:{start_date}..{end_date}&per_page=1"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        while True:
            try:
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    response=handle_api(response,url,headers)
                    if response == None:
                        return False
                break
            except requests.exceptions.SSLError:
                print(f"SSL Error: Redo the request")
        
        response=response.json()  
        
        print(f'{owner}/{repo}, {start_date}..{end_date} - {response["total_count"]} commits')
        
        if response['total_count'] < threshold:
            return False
       
        time.sleep(2) # 30 requests per minute
    
    return True
    
def main():
    """
    Main function to execute the script.
    """
    start_time = time.time()
    repos_dict= {}
    input_file = args.file_input
    
    # Reads the csv file that contains the repositories from Github Search mining tool
    with open(input_file, 'r', encoding='latin-1') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            repo = row[1]
            repo
            commits = row[3]
            repos_dict[repo] = commits
    
    with open("data/projects-accepted.txt", 'w') as output_file:
        for repo, commits in repos_dict.items():
            owner, repo_name = repo.split('/')
            commits_per_interval = search_commits_for_six_months_interval(owner, repo_name, commits)
            
            if commits_per_interval:
                output_file.write(repo + '\n')
            time.sleep(2) # 30 requests per minute
    
    print(f"Execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Given the CSV from GHS, returns the repos '
                                            'that fit all the requirements for the samping')
    parser.add_argument('file_input', type=str, help='The CSV from GHS with at least 10 starts, 10 forks and 12730 commits', default='data/ghs_results.csv')
    parser.add_argument('gh_token', type=str, help='GitHub token for authentication of calls')
    args = parser.parse_args()

    auth_token = args.gh_token
    
    main()