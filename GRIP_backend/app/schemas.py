from pydantic import BaseModel
from typing import List, Dict, Optional
import datetime

# --------------------------------
# Schema for a single commit entry
# --------------------------------
class CommitPayload(BaseModel):
    commit_hash: str
    author: str
    timestamp: datetime.datetime
    message: str
    category: str
    files: List[str]

# --------------------------------
# Schema for file → commits mapping
# --------------------------------
class FileCommitMap(BaseModel):
    files: Dict[str, List[str]]  # e.g. {"core/views.py": ["abc123", "def456"]}

# --------------------------------
# Schema for response after indexing
# --------------------------------
class CommitIndexResponse(BaseModel):
    total_commits: int
    files_indexed: int
    payloads: List[CommitPayload]
