"""
Repository Extractor and Validator

This script extracts repository names from the GHS results CSV file and validates
that they are still accessible on GitHub, filtering out deleted or inaccessible repositories.

Input: ghs_results.csv (from SEART GitHub Search)
Output: projects-accepted.txt (validated repo names, one per line)

Requires: GH_TOKEN environment variable for GitHub API access
"""
import os
import time
import requests
import pandas as pd
import sys
from dotenv import load_dotenv

def extract_and_validate_repos():
    """Extract repository names from CSV and validate they exist on GitHub."""
    
    # Load environment variables
    load_dotenv()
    TOKEN = os.getenv("GH_TOKEN")
    
    if not TOKEN:
        print("Warning: GH_TOKEN environment variable not set. API rate limits will be lower.")
        HEADERS = {}
    else:
        HEADERS = {"Authorization": f"token {TOKEN}"}
    
    # Step 1: Extract repository names from CSV
    print("Step 1: Extracting repository names from CSV...")
    
    if not os.path.exists('ghs_results.csv'):
        print("Error: ghs_results.csv not found in current directory")
        sys.exit(1)
    
    try:
        df = pd.read_csv('ghs_results.csv')
        
        if 'name' not in df.columns:
            print("Error: 'name' column not found in CSV file")
            sys.exit(1)
        
        repo_names = df['name'].tolist()
        print(f"✓ Extracted {len(repo_names)} repository names from CSV")
        
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        sys.exit(1)
    
    # Step 2: Validate repositories on GitHub
    print("\nStep 2: Validating repositories on GitHub...")
    
    final_projects = []
    deleted_count = 0
    
    def fetch_ok(url, retries=2):
        """Fetch URL with retry logic."""
        for i in range(retries + 1):
            try:
                resp = requests.get(url, headers=HEADERS)
            except requests.RequestException as e:
                if i < retries:
                    time.sleep(1)
                    continue
                print(f"[ERROR] Network failure for {url}: {e}")
                return None
            if resp.status_code >= 500 and i < retries:
                time.sleep(1)
                continue
            return resp
        return None
    
    for i, proj in enumerate(repo_names, 1):
        if i % 100 == 0:
            print(f"Progress: {i}/{len(repo_names)} repositories checked")
        
        url = f"https://api.github.com/repos/{proj}"
        resp = fetch_ok(url)
        
        if not resp or not resp.ok:
            code = resp.status_code if resp else "N/A"
            print(f"[REMOVED] {proj} (Status: {code})")
            deleted_count += 1
            continue
        
        final_projects.append(proj)
        
        # Basic rate limiting
        if not TOKEN:  # Unauthenticated requests have lower limits
            time.sleep(0.1)
    
    # Step 3: Save validated repositories
    print(f"\nStep 3: Saving validated repositories...")
    
    with open("projects-accepted.txt", "w") as out:
        for p in final_projects:
            out.write(p + "\\n")
    
    print(f"✓ Validation complete!")
    print(f"  • Original repositories: {len(repo_names)}")
    print(f"  • Removed (deleted/inaccessible): {deleted_count}")
    print(f"  • Valid repositories saved: {len(final_projects)}")
    print(f"  • Output file: projects-accepted.txt")

if __name__ == "__main__":
    extract_and_validate_repos()
