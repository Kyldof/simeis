import os
import urllib.request
import json
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"), encoding="utf-8-sig")

REPO = "Kyldof/simeis"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def fetch_issues():
    issues, page = [], 1
    while True:
        headers = {"Accept": "application/vnd.github+json"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        req = urllib.request.Request(
            f"https://api.github.com/repos/{REPO}/issues?state=all&per_page=100&page={page}",
            headers=headers,
        )
        batch = json.loads(urllib.request.urlopen(req).read())
        if not batch:
            break
        issues += [i for i in batch if "pull_request" not in i]
        page += 1
    return issues


issues = fetch_issues()
open_issues = [i for i in issues if i["state"] == "open"]
closed_issues = [i for i in issues if i["state"] == "closed"]

label_counts = defaultdict(lambda: {"total": 0, "open": 0, "closed": 0})
for issue in issues:
    for lbl in [lb["name"] for lb in issue["labels"]] or ["(sans label)"]:
        label_counts[lbl]["total"] += 1
        label_counts[lbl][issue["state"]] += 1

print(f"Total: {len(issues)}  |  Ouvertes: {len(open_issues)}  |  Fermées: {len(closed_issues)}\n")
print(f"{'Label':<25} {'Total':>6}  {'Ouvertes':>9}  {'Fermées':>8}")
print("-" * 52)
for lbl, c in sorted(label_counts.items(), key=lambda x: -x[1]["total"]):
    print(f"{lbl:<25} {c['total']:>6}  {c['open']:>9}  {c['closed']:>8}")
