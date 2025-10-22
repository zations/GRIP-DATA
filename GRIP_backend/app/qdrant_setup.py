from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from embed import embed_text
import json, time

COLLECTION = "git_commits"
QDRANT_URL = "http://localhost:6333"

client = QdrantClient(QDRANT_URL)

# Ensure collection exists
if COLLECTION not in [c.name for c in client.get_collections().collections]:
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config={"text_vector": VectorParams(size=1024, distance=Distance.COSINE)}
    )

with open("commit_index_enriched.json") as f:
    commits = json.load(f)

batch = []

for commit in commits:
    text = f"{commit['category']} | {commit['message']} | {', '.join(commit['files'])}"
    vector = embed_text(text)
    payload = commit | {"text": text}
    batch.append(
        PointStruct(
            id=hash(commit['commit_hash']) % (10**12),
            vector={"text_vector": vector},
            payload=payload
        )
    )

    if len(batch) >= 50:
        client.upsert(collection_name=COLLECTION, points=batch)
        batch = []
        time.sleep(1)

# Upload any remaining points
if batch:
    client.upsert(collection_name=COLLECTION, points=batch)
