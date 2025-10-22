import os
import json
import boto3
import logging
from dotenv import load_dotenv
from config import EMBED_MODEL

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
EMBED_SOURCE = os.getenv("EMBED_SOURCE", "bedrock").lower()

# Initialize client
_bedrock = None

def bedrock_client():
    """Create or reuse the Bedrock client."""
    global _bedrock
    if _bedrock is None:
        try:
            _bedrock = boto3.client(
                "bedrock-runtime",
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            logger.info("✅ Bedrock client initialized successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Bedrock client: {e}")
            raise
    return _bedrock


def embed_text(text: str):
    """Return a Titan embedding for the given text."""
    text = (text or "").strip()
    if not text:
        return []

    try:
        client = bedrock_client()
        response = client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps({"inputText": text}),
            accept="application/json",
            contentType="application/json",
        )
        body = json.loads(response["body"].read())
        return body["embedding"]
    except client.exceptions.AccessDeniedException:
        logger.error("Access denied. Check if Titan Embeddings is enabled in your AWS console.")
        return []
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        return []
