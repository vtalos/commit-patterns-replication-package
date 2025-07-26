import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GH_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

with open("projects-accepted.txt") as f:
    original = [line.strip() for line in f if line.strip()]

final_projects = []

def fetch_ok(url, retries=2):
    for i in range(retries+1):
        try:
            resp = requests.get(url, headers=HEADERS)
        except requests.RequestException as e:
            if i < retries:
                time.sleep(1)
                continue
            print(f"[ERROR] Network failure: {e}")
            return None
        if resp.status_code >= 500 and i < retries:
            time.sleep(1)
            continue
        return resp
    return None

for proj in original:
    url = f"https://api.github.com/repos/{proj}"
    resp = fetch_ok(url)
    if not resp or not resp.ok:
        code = resp.status_code if resp else "N/A"
        print(f"[ERROR {code}] {proj}")
        continue

    final_projects.append(proj)

with open("projects-accepted-checked.txt", "w") as out:
    for p in final_projects:
        out.write(p + "\n")
