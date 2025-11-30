import wikipedia
import re
from utils.logger import log_info, log_error
from utils.storage import get_vector_store
from utils.embedding import extract_context, get_relevant_chunks


def get_wiki_pages(query: str, count: int=5, lang: str="de") -> list:
    if not query:
        return []
    try:
        wikipedia.set_lang(lang)
        results = wikipedia.search(query, results=count)
        log_info(f"Found {len(results)} pages for topic '{query}' and language '{lang}': {results}")
        return results
    except Exception as e:
        return [f"Error while searching the Wikipedia pages for topic '{query}' and language '{lang}': {e}"]

def get_content_for_wiki_page(title: str, lang: str="de") -> str:
    try:
        wikipedia.set_lang(lang)
        page = wikipedia.page(title, auto_suggest=False)
        text = page.content
        text = re.sub(r"==+.*?==+", "", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text.strip())
        log_info(f"Extracted content of length {len(text)} for page '{title}'")
        return text.strip()
    except Exception as e:
        return f"Error while loading the Wikipedia page '{title}' for language '{lang}': {e}"

def query_wikipedia(topic: str, query: str, language: str) -> str:
    top_n = 3
    try:
        pages = get_wiki_pages(topic, 1, language)
        if not pages:
            log_error(f"Page for topic '{topic}' not found")
            return f"Page for topic '{topic}' not found"

        collection = get_vector_store()
        content = get_content_for_wiki_page(pages[0], language)
        uid = extract_context(collection, pages[0], content, language, "wikipedia")
        chunks = get_relevant_chunks(collection, query, top_n, [uid])

        log_info(f"Collected the {top_n} most relevant chunks for query '{query}'")
        return "\n\n".join(chunks)
    except Exception as e:
        log_error(str(e))
        return f"Something went wrong: {e}"