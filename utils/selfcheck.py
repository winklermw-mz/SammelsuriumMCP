import requests
from utils.config import LLM_URL, CHROMADB_HOST, CHROMADB_PORT
from utils.logger import log_error, log_info

def check_url(service: str, url: str):
    try:
        log_info(f"Checking {service}...")
        response = requests.get(url)
        response.raise_for_status()
        log_info(f"successfully connected to {service}, status code: " + str(response.status_code))
        return True
    except requests.exceptions.RequestException as e:
        log_error("Connection error:" + str(e))
        return False

def perform_checkup() -> bool:
    return check_url("ChromaDB", f"http://{CHROMADB_HOST}:{CHROMADB_PORT}/api/v2/heartbeat") \
        and check_url("LM Studio", f"{LLM_URL}/v1/heartbeat")

if __name__ == "__main__":
    perform_checkup()