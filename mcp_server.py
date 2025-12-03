from fastmcp import FastMCP
from datetime import datetime
from typing import Annotated
from tools.weather.forecast import get_weather_forecast
from tools.search.duckduckgo import web_search
from tools.search.wiki import query_wikipedia
from tools.search.document import query_document
from tools.calendar.google import get_all_calendar_entries, get_all_available_calendars
from utils.storage import get_vector_store, get_aggregated_documents
from utils.config import SERVER_IP, SERVER_PORT


mcp = FastMCP("MyMCP")

@mcp.tool(description="Returns the current weather forecast for a given location")
def get_current_weather(location: str) -> dict:
    try:
        return get_weather_forecast(location)
    except Exception as e:
        return {"error": f"Something went wrong: {e}"}

@mcp.tool(description="To query unknown or recent data this tool can be used to search the internet")
def search_web(query: str) -> str:
    try:
        return web_search(query)
    except Exception as e:
        return f"Something went wrong: {e}"
    
@mcp.tool(description="Get more information about a specific topic from Wikipedia to answer the user query")
def search_wikipedia(
    topic: Annotated[str, "Topic to be searched for in Wikipedia. Since only one topic can be selected, it should be as concise as possible. For example, 'London' if you are looking for sights in London."], 
    query: Annotated[str, "Question that the user wants to answer with the help of Wikipedia"]
) -> str:
    return query_wikipedia(topic, query, "de")
    
@mcp.tool(description="Load a file from the local computer to answer the user's question")
def read_file(
    filename: Annotated[str, "Name of the local file to be read"], 
    query: Annotated[str, "Question that the user wants to answer with the local document"]
) -> str:
    try:
        return query_document(filename, query)
    except Exception as e:
        return f"Something went wrong: {e}"
    
@mcp.tool(description="Returns a comma separated list of all available calendars.")
def get_available_calendars() -> str:
    try:
        return get_all_available_calendars()
    except Exception as e:
        return f"Something went wrong: {e}"

@mcp.tool(description="Returns all entries of a specific calendar for the next N days.")
def get_calendar_entries(
    calendar_name: Annotated[str, "Name of the calendar to use"], 
    days: Annotated[int, "Number of days to look for in the given calendar"]
) -> str:
    try:
        return get_all_calendar_entries(calendar_name, days)
    except Exception as e:
        return f"Something went wrong: {e}"

@mcp.tool(description="Returns the current date")
def get_current_date() -> str:
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    return f"Today's date is {current_date}"

@mcp.tool(description="Returns the current location of the user")
def get_current_location() -> str:
    return "The user is located in Mainz, Germany"


if __name__ == "__main__":
    collection = get_vector_store()
    get_aggregated_documents(collection)
    
    mcp.run(transport="http", host=SERVER_IP, port=SERVER_PORT)