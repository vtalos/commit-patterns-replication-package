"""
GitHub Repository Information Scraper

This script reads a list of GitHub repositories from a text file and retrieves
information about each repository using the GitHub REST API.

Required: pip install requests
Optional: Set GITHUB_TOKEN environment variable for higher rate limits
"""
import requests
import csv
import time
import os
import sys
from typing import Dict, Optional, List

if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

class GitHubScraper:
    def __init__(self, token: Optional[str] = None):
        """Initialize the GitHub scraper with optional authentication token."""
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        
        # Set up authentication if token is provided
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})
        
        # Rate limiting
        self.requests_made = 0
        self.rate_limit_remaining = 60  # Default for unauthenticated requests
        
    def get_rate_limit_info(self) -> Dict:
        """Get current rate limit information."""
        response = self.session.get(f"{self.base_url}/rate_limit")
        if response.status_code == 200:
            return response.json()
        return {}
    
    def wait_for_rate_limit(self):
        """Wait if we're approaching rate limits."""
        if self.rate_limit_remaining <= 5:
            print("Approaching rate limit. Waiting 60 seconds...")
            time.sleep(60)
            rate_info = self.get_rate_limit_info()
            if 'resources' in rate_info:
                self.rate_limit_remaining = rate_info['resources']['core']['remaining']
    
    def get_repo_info(self, owner: str, repo: str) -> Dict:
        """Get basic repository information."""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = self.session.get(url)
        
        # Update rate limit info from headers
        if 'X-RateLimit-Remaining' in response.headers:
            self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Repository {owner}/{repo} not found")
            return {}
        else:
            print(f"Error fetching {owner}/{repo}: {response.status_code}")
            return {}
    
    def get_contributors_count(self, owner: str, repo: str) -> int:
        """Get the number of contributors to the repository."""
        # GitHub API paginates contributors, we need to count them properly
        url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
        contributors = 0
        page = 1
        
        while True:
            self.wait_for_rate_limit()
            response = self.session.get(url, params={'page': page, 'per_page': 100})
            
            if 'X-RateLimit-Remaining' in response.headers:
                self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
            
            if response.status_code != 200:
                print(f"Error fetching contributors for {owner}/{repo}: {response.status_code}")
                break
                
            data = response.json()
            if not data:  # Empty page means we've reached the end
                break
                
            contributors += len(data)
            page += 1
            
            # Safety check to avoid infinite loops
            if page > 100:  # Assuming no repo has more than 10,000 contributors
                print(f"Warning: {owner}/{repo} has many contributors, stopping count at {contributors}")
                break
        
        return contributors
    
    def get_commits_count(self, owner: str, repo: str) -> int:
        """Get the total number of commits in the repository."""
        # Use the commits endpoint to get commit count
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        
        # First, try to get the first page to see if there are any commits
        self.wait_for_rate_limit()
        response = self.session.get(url, params={'per_page': 1})
        
        if 'X-RateLimit-Remaining' in response.headers:
            self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
        
        if response.status_code != 200:
            print(f"Error fetching commits for {owner}/{repo}: {response.status_code}")
            return 0
        
        # Check if there's a Link header with pagination info
        link_header = response.headers.get('Link', '')
        if 'rel="last"' in link_header:
            # Extract the last page number from the Link header
            import re
            last_page_match = re.search(r'page=(\d+)>; rel="last"', link_header)
            if last_page_match:
                last_page = int(last_page_match.group(1))
                
                # Get the last page to count remaining commits
                self.wait_for_rate_limit()
                last_response = self.session.get(url, params={'page': last_page, 'per_page': 100})
                if last_response.status_code == 200:
                    last_page_commits = len(last_response.json())
                    total_commits = (last_page - 1) * 100 + last_page_commits
                    return total_commits
        
        # If no pagination, count the commits in the response
        commits = response.json()
        return len(commits) if commits else 0
    
    def get_languages(self, owner: str, repo: str) -> str:
        """Get the primary programming language of the repository."""
        url = f"{self.base_url}/repos/{owner}/{repo}/languages"
        
        self.wait_for_rate_limit()
        response = self.session.get(url)
        
        if 'X-RateLimit-Remaining' in response.headers:
            self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
        
        if response.status_code == 200:
            languages = response.json()
            if languages:
                # Return the language with the most bytes of code
                return max(languages.items(), key=lambda x: x[1])[0]
        
        return "Unknown"
    
    def scrape_repository(self, repo_string: str) -> Dict:
        """Scrape all information for a single repository."""
        try:
            owner, repo = repo_string.strip().split('/', 1)
        except ValueError:
            print(f"Invalid repository format: {repo_string}")
            return {}
        
        print(f"Scraping {owner}/{repo}...")
        
        # Get basic repo info
        repo_info = self.get_repo_info(owner, repo)
        if not repo_info:
            return {}
        
        # Extract basic information
        result = {
            'repository': f"{owner}/{repo}",
            'size_kb': repo_info.get('size', 0),
            'stars': repo_info.get('stargazers_count', 0),
            'language': repo_info.get('language', 'Unknown')
        }
        
        # Get contributors count (this requires additional API calls)
        time.sleep(0.1)  # Small delay to be respectful
        result['contributors'] = self.get_contributors_count(owner, repo)
        
        # Get commits count (this also requires additional API calls)
        time.sleep(0.1)  # Small delay to be respectful
        result['commits'] = self.get_commits_count(owner, repo)
        
        return result


def read_repositories(filename: str) -> List[str]:
    """Read repository names from a text file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            repos = [line.strip() for line in f if line.strip()]
        return repos
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return []


def save_to_csv(data: List[Dict], filename: str):
    """Save the scraped data to a CSV file."""
    if not data:
        print("No data to save.")
        return
    
    fieldnames = ['repository', 'size_kb', 'contributors', 'commits', 'stars', 'language']
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def main():
    """Main function to run the scraper."""
    if len(sys.argv) != 2:
        print("Usage: python github_scraper.py <input_file.txt>")
        print("Example: python github_scraper.py repositories.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = input_file.rsplit('.', 1)[0] + '_info.csv'
    
    # Get GitHub token from environment variable (optional but recommended)
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Warning: No GITHUB_TOKEN environment variable found.")
        print("You'll be limited to 60 requests per hour. Consider creating a personal access token.")
        print("See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token")
    
    # Read repositories from file
    repositories = read_repositories(input_file)
    if not repositories:
        print("No repositories to process.")
        sys.exit(1)
    
    print(f"Found {len(repositories)} repositories to process.")
    
    # Initialize scraper
    scraper = GitHubScraper(github_token)
    
    # Show current rate limit
    rate_info = scraper.get_rate_limit_info()
    if 'resources' in rate_info:
        remaining = rate_info['resources']['core']['remaining']
        print(f"Rate limit remaining: {remaining}")
    
    # Scrape each repository
    results = []
    for i, repo in enumerate(repositories, 1):
        print(f"Processing {i}/{len(repositories)}: {repo}")
        
        result = scraper.scrape_repository(repo)
        if result:
            results.append(result)
            print(f"✓ Success: {repo}")
        else:
            print(f"✗ Failed: {repo}")
        
        # Add delay between repositories to be respectful
        if i < len(repositories):
            time.sleep(1)
    
    # Save results to CSV
    if results:
        save_to_csv(results, output_file)
        print(f"\nCompleted! Processed {len(results)} repositories successfully.")
        print(f"Results saved to: {output_file}")
    else:
        print("\nNo repositories were successfully processed.")


if __name__ == "__main__":
    main()