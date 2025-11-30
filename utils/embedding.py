from openai import OpenAI
from utils.storage import Collection
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.logger import log_debug, log_info, log_error
from utils.storage import store_document, is_already_stored, execute_query

TOP_N = 5
CHUNK_SIZE = 500
CHUNK_OVERLAP = 0
CHUNK_THRESHOLD = 150
EMBEDDING_MODEL = "text-embedding-jina-embeddings-v2-base-de"

# creates a set of chunks from the given text
def create_chunks(text: str) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ".", "!", "?", ";", " ", ""]
    )

    chunks = text_splitter.split_text(text)
    all_chunks = []
    current_chunk = ""

    for chunk in chunks:
        if len(chunk) < CHUNK_THRESHOLD:
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
    client = OpenAI(base_url="http://host.docker.internal:1234/v1", api_key="lm-studio")
    response = client.embeddings.create(input=chunk, model=EMBEDDING_MODEL)
    return response.data[0].embedding

# returns the top-N most relevant chunks for the given user query
def get_relevant_chunks(my_store: Collection, query: str, top_n: int, sources: list) -> list:
    if len(sources):
        results = execute_query(my_store, _create_embedding(query), top_n, {"source": {"$in": sources}})
    else:
        results = execute_query(my_store, _create_embedding(query), top_n)
    
    return results["documents"][0]

# extracts the content from given page, find the N most relevant
# chunks for the given user prompt and adds those as additional context to the prompt
def extract_context(my_store: Collection, page: str, content: str, lang: str="de", prefix: str="url") -> str: 
    uid = f"{prefix}**{lang}**{page}"
    chunks = []

    if not is_already_stored(my_store, {"source": uid}):
        if content.startswith("🔥 Error"):
            log_error(content)
            return content

        chunks = create_chunks(content)
        log_info(f"Extracted {len(chunks)} chunks from page '{page}'")

        for chunk_id, chunk in enumerate(chunks):
            embedding = _create_embedding(chunk)
            store_document(my_store, f"{page}-{chunk_id}", chunk, embedding, {"source": uid})
    else:
        log_info(f"Page '{page}' has already been read")

    return uid
