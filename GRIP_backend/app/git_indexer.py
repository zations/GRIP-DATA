# app/git_indexer.py
from pathlib import Path
from git import Repo
import datetime
import subprocess
from typing import List
from collections import defaultdict
import json

from schemas import CommitPayload, CommitIndexResponse
import re

def filter_valid_files(file_list):
    """
    Filter out unwanted or system-related files from a commit.
    Works across nested directories and OS paths.
    """
    EXCLUDED_PATTERNS = [
        r"(^|/)__pycache__",       # exclude any pycache folder
        r"\.pyc$",            # compiled Python files
        r"\.pyo$",            # optimized bytecode
        r"\.sqlite3$",        # SQLite DB files
        r"(^|/)myenv/",       # your virtual environment
        r"(^|/)Lib/",         # Windows site-packages
        r"site-packages",     # pip installed libs
    ]
    
    def is_valid_file(f):
        normalized = f.replace("\\", "/")  # normalize Windows paths
        return not any(re.search(pat, normalized) for pat in EXCLUDED_PATTERNS)

    return [f for f in file_list if is_valid_file(f)]
# -----------------------------
# Commit Categorizer
# -----------------------------
def categorize_commit(message: str) -> str:
    """Simple classifier for commit messages."""
    m = (message or "").strip().lower()
    if m.startswith("(fix)"):
        return "fix"
    if m.startswith("(error)"):
        return "error"
    if m.startswith(("(feature)", "(feat)")):
        return "feature"
    return "other"


# -----------------------------
# Repo Validation
# -----------------------------
def verify_repo(repo_path: str):
    """Ensure this folder actually contains a .git repo."""
    if not (Path(repo_path) / ".git").exists():
        raise ValueError(f"❌ No .git found in {repo_path}. Check the correct repo path.")


# -----------------------------
# Get Visible Commits (same as `git log`)
# -----------------------------
def get_git_commits(repo_path: str) -> List[str]:
    """Return commit hashes visible on current branch."""
    result = subprocess.run(
        ["git", "log", "--pretty=format:%H"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )
    commits = result.stdout.strip().splitlines()
    print(f"🔍 Found {len(commits)} commits from visible history")
    return commits


# -----------------------------
# Iterate Over Commits (flat file-based)
# -----------------------------
def iter_commit_points(repo_path: str, commit_hashes: List[str]):
    """Yield each commit’s metadata and affected files."""
    repo = Repo(repo_path)
    seen = set()

    for commit_hash in commit_hashes:
        c = repo.commit(commit_hash)
        short_hash = c.hexsha[:8]

        if short_hash in seen:
            continue
        seen.add(short_hash)

        msg = (c.message or "").strip()

        # Filter unwanted paths
        raw_files = list(c.stats.files.keys())
        files = filter_valid_files(raw_files)

        if not files:
            continue

        payload = CommitPayload(
            commit_hash=c.hexsha,
            author=getattr(c.author, "name", "unknown"),
            timestamp=datetime.datetime.fromtimestamp(c.committed_date),
            message=msg,
            category=categorize_commit(msg),
            files=files,
        )

        yield int(c.committed_date), payload


# -----------------------------
# Build Commit Index
# -----------------------------
def build_commit_index(repo_path: str, save_json: bool = True) -> CommitIndexResponse:
    repo = Repo(repo_path)
    commit_hashes = [c.hexsha for c in repo.iter_commits()]
    file_commit_map = defaultdict(list)
    commit_payloads: List[dict] = []
    seen = set()

    for commit_hash in commit_hashes:
        c = repo.commit(commit_hash)
        short_hash = c.hexsha[:8]

        if short_hash in seen:
            continue
        seen.add(short_hash)

        msg = (c.message or "").strip()
        category = categorize_commit(msg)
        raw_files = list(c.stats.files.keys())
        files = filter_valid_files(raw_files)

        if not files:
            continue

        # ✅ This is your final commit record (one JSON object per commit)
        payload = {
            "commit_hash": c.hexsha,
            "author": getattr(c.author, "name", "unknown"),
            "timestamp": datetime.datetime.fromtimestamp(c.committed_date).isoformat(),
            "message": msg,
            "category": category,
            "files": files,
        }

        commit_payloads.append(payload)

        # Still build reverse lookup (file → commits)
        for f in files:
            file_commit_map[f].append(c.hexsha)

    # ✅ Save in the final flat format
    if save_json:
        with open("commit_index_enriched.json", "w") as f:
            json.dump(commit_payloads, f, indent=2)

    print(f"✅ Indexed {len(commit_payloads)} commits")
    print(f"📄 Files tracked: {len(file_commit_map)}")

    return CommitIndexResponse(
        total_commits=len(commit_payloads),
        files_indexed=len(file_commit_map),
        payloads=commit_payloads,
    )

# -----------------------------
# Debug / Print Mode
# -----------------------------
if __name__ == "__main__":
    repo_path = "C:\Users\pavit\programing\GRIP\grip"
    verify_repo(repo_path)

    response = build_commit_index(repo_path)

    print(f"\n🔎 {response.total_commits} commits indexed.\n")

    for i, payload in enumerate(response.payloads, start=1):
        print(f"🧩 Commit {i}: {payload.commit_hash[:8]} | {payload.category}")
        print(f"   Author: {payload.author}")
        print(f"   Date: {payload.timestamp}")
        print(f"   Files affected:")
        for f in payload.files:
            print(f"     └── {f}")
        print(f"   Message: {payload.message}")
        print("-" * 70)
