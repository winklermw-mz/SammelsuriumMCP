import pymupdf
from utils.logger import log_info, log_error
from utils.storage import get_vector_store
from utils.embedding import extract_context, get_relevant_chunks
from utils.config import RAG_TOP_N, DOCUMENT_ROOT
from pathlib import Path


def _find_all_files(filename, search_path) -> list:
    root = Path(search_path)
    return list(root.rglob(filename))

def _extract_content(filename: str) -> str:
    doc = pymupdf.open(filename)
    text = ""
    for page in doc:
        text += str(page.get_text())
    return text

def query_document(filename: str, query: str) -> str:
    collection = get_vector_store()
    uid = read_document(collection, filename)
    chunks = get_relevant_chunks(collection, query, RAG_TOP_N, [uid])

    log_info(f"Collected the {RAG_TOP_N} most relevant chunks for query '{query}'")
    return "\n\n".join(chunks)

def read_document(collection, filename: str) -> str:
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

    content = _extract_content(file)
    return extract_context(collection, file, content, "-", "File")