from git import Repo
import json
import datetime
from git_indexer import categorize_commit, filter_valid_files

repo_path = r"C:\Users\pavit\programing\GRIP\grip"

# Load your file → commit mapping
with open("commit_index.json", "r") as f:
    file_commit_map = json.load(f)["files"]

# Flatten all unique commits
unique_commits = set()
for commits in file_commit_map.values():
    unique_commits.update(commits)

print(f"📦 Found {len(unique_commits)} unique commits")

repo = Repo(repo_path)
commit_metadata = []

for commit_hash in unique_commits:
    c = repo.commit(commit_hash)
    msg = (c.message or "").strip()
    category = categorize_commit(msg)
    raw_files = list(c.stats.files.keys())
    files = filter_valid_files(raw_files)  

    commit_metadata.append({
        "commit_hash": c.hexsha,
        "author": getattr(c.author, "name", "unknown"),
        "timestamp": datetime.datetime.fromtimestamp(c.committed_date).isoformat(),
        "message": msg,
        "category": category,
        "files": files
    })

# Save full commit data
print(commit_metadata)
with open("commit_metadata.json", "w") as f:
    json.dump(commit_metadata, f, indent=2)

print("✅ commit_metadata.json generated successfully!")
