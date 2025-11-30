import requests
import re
from bs4 import BeautifulSoup
from ddgs import DDGS
from utils.storage import get_vector_store
from utils.embedding import extract_context, get_relevant_chunks
from utils.logger import log_error, log_info
from utils.config import RAG_TOP_N


def extract_text(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
    except:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="")
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text

def get_content(query: str, top_n: int) -> dict:
    pages = {}
    response = DDGS().text(query=query, max_results=top_n, region="de-de")
    for resp in response:
        url = resp.get("href")
        pages[url] = extract_text(url)
    return pages

def web_search(query: str) -> str:
    try:
        collection = get_vector_store()
        pages = get_content(query, RAG_TOP_N)
        uids = []

        for url, content in pages.items():
            uids.append(extract_context(collection, url, content, "de", "Web"))
        
        chunks = get_relevant_chunks(collection, query, RAG_TOP_N, uids)

        log_info(f"Collected the {RAG_TOP_N} most relevant chunks for query '{query}'")
        return "\n\n".join(chunks)
    except Exception as e:
        log_error(str(e))
        return f"Something went wrong: {e}"