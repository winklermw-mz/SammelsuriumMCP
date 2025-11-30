import pymupdf
from utils.logger import log_info, log_error
from utils.storage import get_vector_store
from utils.embedding import extract_context, get_relevant_chunks
from utils.config import RAG_TOP_N
from pathlib import Path


DOCUMENT_ROOT = "/documents"

def _find_all_files(filename, search_path) -> list:
    root = Path(search_path)
    return list(root.rglob(filename))

def _extract_content(filename: str) -> str:
    doc = pymupdf.open(filename)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def query_document(filename: str, query: str) -> str:
    files = _find_all_files(filename, DOCUMENT_ROOT)

    if len(files) == 0:
        log_error(f"Error: File '{filename}' not found below '{DOCUMENT_ROOT}'")
        raise Exception(f"Error: File '{filename}' not found")
    elif len(files) > 1:
        log_error(f"Error: Found more than one file with name '{filename}'")
        raise Exception(f"Error: More than one file '{filename}' found")
    else:
        file = files[0]
        log_info(f"Found document '{file}'")

    collection = get_vector_store()
    content = _extract_content(file)
    uid = extract_context(collection, file, content, "-", "File")
    chunks = get_relevant_chunks(collection, query, RAG_TOP_N, [uid])

    log_info(f"Collected the {RAG_TOP_N} most relevant chunks for query '{query}'")
    return "\n\n".join(chunks)
