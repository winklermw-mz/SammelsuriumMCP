import requests
import json
from utils.storage import Collection
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.logger import log_debug, log_info, log_error
from utils.storage import store_document, is_already_stored, execute_query
from utils.config import LLM_URL, LLM_API_KEY, EMBEDDING_MODEL, EMBEDDING_CHUNK_SIZE, EMBEDDING_CHUNK_OVERLAP, EMBEDDING_CHUNK_THRESHOLD


# creates a set of chunks from the given text
def create_chunks(text: str) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=EMBEDDING_CHUNK_SIZE,
        chunk_overlap=EMBEDDING_CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ".", "!", "?", ";", " ", ""]
    )

    chunks = text_splitter.split_text(text)
    all_chunks = []
    current_chunk = ""

    for chunk in chunks:
        if len(chunk) < EMBEDDING_CHUNK_THRESHOLD:
            current_chunk = (current_chunk + " " + chunk).strip()
        else:
            if current_chunk:
                all_chunks.append(current_chunk)
            current_chunk = chunk
    if current_chunk:
        all_chunks.append(current_chunk)

    for chunk_id, chunk in enumerate(all_chunks):
        log_debug(f"Chunk #{chunk_id}: {chunk}".replace("\n", " "))

    return all_chunks

# creates an embedding vector for the given chunk
def _create_embedding(chunk: str) -> list:
    response = requests.post(
        f"{LLM_URL}/embedding", 
        headers={"Content-Type": "application/json"}, 
        data=json.dumps(chunk)
    )
    return json.loads(response.text)

# returns the top-N most relevant chunks for the given user query
def get_relevant_chunks(my_store: Collection, query: str, top_n: int, sources: list) -> list:
    if len(sources):
        results = execute_query(my_store, _create_embedding(query), top_n, {"source": {"$in": sources}})
    else:
        results = execute_query(my_store, _create_embedding(query), top_n)
    
    return results["documents"][0]

# returns a unique id for the given document
def _get_uid(doc: str, type: str="url", lang: str="de") -> str:
    return f"[{type}] {doc} --lang={lang}"

# extracts the content from given document, find the N most relevant
# chunks for the given user prompt and adds those as additional context to the prompt
def extract_context(my_store: Collection, doc: str, content: str, lang: str="de", prefix: str="url") -> str: 
    uid = _get_uid(doc, prefix, lang)
    chunks = []

    if not is_already_stored(my_store, {"source": uid}):
        if content.startswith("🔥 Error"):
            log_error(content)
            return content

        chunks = create_chunks(content)
        log_info(f"Extracted {len(chunks)} chunks from doc '{doc}'")

        for chunk_id, chunk in enumerate(chunks):
            embedding = _create_embedding(chunk)
            store_document(my_store, f"{doc}-{chunk_id}", chunk, embedding, {"source": uid})
    else:
        log_info(f"Document '{doc}' has already been read")

    return uid
