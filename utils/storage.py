import chromadb
from chromadb import Collection
from chromadb.config import Settings
from utils.logger import log_info, log_debug

HOST_NAME = "localhost"
PORT = 8000
STORAGE_NAME = "my-mcp-rag"

store = None

# create or retrieve a persistent instance of the ChromaDB vector store
def get_vector_store(collection: str = STORAGE_NAME, reset: bool = False) -> Collection:
    global store
    if store == None or reset:
        client = chromadb.HttpClient(host=HOST_NAME, port=PORT, settings=Settings(allow_reset=False))
        if reset: 
            try:
                client.delete_collection(name=collection)
            except:
                pass

        store = client.get_or_create_collection(name=collection)
    return store

# stores the given chunk and its embedding vector in the vector store
def store_document(my_store: Collection, id: str, chunk: str, embedding: list, metadata: dict):
    my_store.add(ids=[id], documents=[chunk], embeddings=[embedding], metadatas=[metadata])

# checks if documents has already been stored
def is_already_stored(my_store: Collection, where: dict) -> bool:
    results = my_store.get(where=where)
    return len(results['ids']) > 0

# get N most relevant chunks for given embedding and the provided restriction
def execute_query(my_store: Collection, embedding: list, top_n: int, where: dict|None = None) -> list: 
    if not where:
        return my_store.query(query_embeddings=[embedding], n_results=top_n)
    return my_store.query(query_embeddings=[embedding], n_results=top_n, where=where)

# returns the number of already indexed chunks per source
def get_aggregated_documents(my_store: Collection) -> list:
    limit = 1000
    offset = 0
    categories = {}

    while True:
        batch = my_store.get(include=["metadatas"], limit=limit, offset=offset)
        if not batch["ids"]: break
        for meta in batch["metadatas"]:
            if meta and "source" in meta:
                if meta["source"] not in categories:
                    categories[meta["source"]] = 0
                categories[meta["source"]] += 1
        offset += limit

    log_info(f"Already stored {len(categories)} files and pages")
    for category, count in categories.items():
        log_debug(f"'{category}' with {count} chunks")
