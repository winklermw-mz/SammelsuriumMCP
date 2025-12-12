import requests
from utils.config import LLM_URL, CHROMADB_HOST, CHROMADB_PORT

def check_url(service: str, url: str):
    try:
        print(f"Checking {service}...", end=" ")
        response = requests.get(url)
        response.raise_for_status()
        print("successfully connected, status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("connection error:", e)

if __name__ == "__main__":
    check_url("ChromaDB", f"http://{CHROMADB_HOST}:{CHROMADB_PORT}/api/v2/heartbeat")
    check_url("LM Studio", f"{LLM_URL}/models")