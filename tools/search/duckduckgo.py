from ddgs import DDGS

def web_search(query: str) -> dict:
    pages = DDGS().text(query, max_results=5, region="de-de")
    result = []
    for page in pages:
        result.append(f"{page["title"]}: {page["body"]}")
    return "\n\n".join(result)
