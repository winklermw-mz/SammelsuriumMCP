from tools.search.document import read_document
from utils.config import GENAI_KNOWLEDGE_BASE, RAG_TOP_N
from utils.storage import get_vector_store
from utils.embedding import get_relevant_chunks
from utils.logger import log_info


def query_genai_knowledge_base(question: str) -> str:
    uids = []
    collection = get_vector_store()
    
    for filename in GENAI_KNOWLEDGE_BASE:
        uids.append(read_document(collection, filename))
    
    chunks = get_relevant_chunks(collection, question, RAG_TOP_N, uids)

    log_info(f"Collected the {RAG_TOP_N} most relevant chunks for query '{question}'")
    return "\n\n".join(chunks)