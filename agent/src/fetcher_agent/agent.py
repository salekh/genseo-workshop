from google.adk import Agent as AdkAgent
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams, SseConnectionParams
from mcp.client.stdio import StdioServerParameters
from dotenv import load_dotenv
import os

class FetcherAgent(AdkAgent):
    """
    Agent specialized in fetching website content using MCP.
    """
    def __init__(self):
        
        # Initialize MCPToolset with the fetch server configuration
        load_dotenv()
        
        mcp_tools = MCPToolset(
            connection_params=SseConnectionParams(
                url=os.getenv("FETCHER_MCP_URL"),
            )
        )
        
        super().__init__(
            name="FetcherAgent",
            model="gemini-3-flash-preview",
            description="Fetches website content.",
            tools=[mcp_tools]
        )

# Expose root_agent for ADK loader
root_agent = FetcherAgent()
