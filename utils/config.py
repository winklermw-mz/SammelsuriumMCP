DEBUG = False

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8002

LLM_URL = "http://host.docker.internal:8001"
LLM_API_KEY = "lm-studio"

EMBEDDING_MODEL = "text-embedding-jina-embeddings-v2-base-de"
EMBEDDING_CHUNK_SIZE = 500
EMBEDDING_CHUNK_OVERLAP = 0
EMBEDDING_CHUNK_THRESHOLD = 150

CHROMADB_HOST = "ChromaDB"
CHROMADB_PORT = 8000
CHROMADB_COLLECTION = "my-mcp-rag"

RAG_TOP_N = 3

DOCUMENT_ROOT = "/documents"

GOOGLE_SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
GOOGLE_TOKEN = "auth/token.json"
GOOGLE_CREDENTIALS = "auth/credentials.json"

MY_LOCATION = "Mainz, Germany"