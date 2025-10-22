import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
EMBED_MODEL = os.getenv("EMBED_MODEL", "amazon.titan-embed-text-v1")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

COMMITS_COLLECTION = "commits_static"
ERRORS_COLLECTION = "errors_live"
VECTOR_SIZE = 1536  # Titan embeddings size
