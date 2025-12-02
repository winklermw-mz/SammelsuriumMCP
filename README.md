# MCP Server

This is a simple server application built using FastMCP, designed to handle various tools for retrieving information such as weather forecasts, web searches, Wikipedia queries, and more. Using these tools a local small LLM can be used with more recent data.

## Provided Tools

- `execute_web_search`: Performs internet searches to query unknown or recent data using DuckDuckGo.
- `search_wikipedia`: Queries Wikipedia for more detailed information on specific topics.
- `read_file`: Extract information from a local PDF file.
- `get_available_calendars`: Lists all available Google calendars. (*)
- `get_calendar_entries`: Lists all calendar entries for a specific calendar for the next N days. (*)
- `get_current_weather`: Retrieves the current weather forecast for a given location.
- `get_current_date`: Returns the current date in a formatted string.
- `get_current_location`: Returns the fixed location of the user (currently set to Mainz, Germany).

(\*) Please note, that you need to create a valid Google access token before using the tool for the first time, see <https://developers.google.com/identity/protocols/oauth2?hl=en> for details.

## Requirements

- Python 3.x; please note, that at the time of writing Python 3.14 is not compatible with ChromaDB thus Python 3.12 is used instead
- FastMCP
- ChromaDB, modify `utils.config.py` for configuration of host and port as ChromaDB is supposed to be available in a separate docker container by default
- OpenAI compatible LLM, modify `utils.config.py` if necessary
- PyMuPDF
- Other dependencies as specified in `requirements.txt`

## Installation

1. Clone or download this repository.
2. Ensure all required dependencies are installed.

```bash
pip install fastmcp requests ddgs beautifulsoup4 chromadb wikipedia colorama langchain-text-splitters openai pymupdf google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

3. Run the server:

```bash
python mcp_server.py
```

## Usage

The MCP Server runs on `http://0.0.0.0:7999/mcp`. You can interact with the server using the provided tools.

## Docker

The server can be run in a docker container. A docker file as well as a setup script `create_docker_image.sh` is available.
