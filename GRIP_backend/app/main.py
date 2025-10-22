import os
from dotenv import load_dotenv
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

COMMITS_COLLECTION = "commits_static"
ERRORS_COLLECTION  = "errors_live"
VECTOR_SIZE        = 782
