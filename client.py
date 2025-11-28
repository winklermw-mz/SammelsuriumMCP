import asyncio
from fastmcp import Client
from mcp_server import mcp

async def test_tools():
    client = Client(mcp)
    
    async with client:
        result = await client.call_tool("get_current_weather", {"location": "Mainz"})
        print(result)

    async with client:
        result = await client.call_tool("execute_web_search", {"query": "Wer ist Nino Haase?"})
        print(result)

    async with client:
        result = await client.call_tool("get_current_date", {})
        print(result)

if __name__ == "__main__":
    asyncio.run(test_tools())