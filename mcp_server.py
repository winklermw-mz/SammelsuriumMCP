from fastmcp import FastMCP
from datetime import datetime

from tools.weather.forecast import get_weather_forecast
from tools.search.duckduckgo import web_search


mcp = FastMCP("Test MCP Server")

@mcp.tool(description="Returns the current weather forecast for a given location")
def get_current_weather(location: str) -> dict:
    try:
        return get_weather_forecast(location)
    except Exception as e:
        return {"error": f"Something went wrong: {e}"}

@mcp.tool(description="Executes a web search with the given user query")
def execute_web_search(query: str) -> str:
    try:
        return web_search(query)
    except Exception as e:
        return f"Something went wrong: {e}"
    
@mcp.tool(description="Returns the current date")
def get_current_date() -> str:
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    return f"Today's date is {current_date}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)