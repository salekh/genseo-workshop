from typing import Dict, Any
from google.adk.tools import FunctionTool
from tools.google_ads import GoogleAdsClient
from tools.serp_api import SerpApiClient
from tools.custom_search import CustomSearchClient
from config import settings

def get_keyword_ideas(topic: str) -> Dict[str, Any]:
    """
    Retrieves keyword ideas and metrics for a given topic using Google Ads API.
    
    Args:
        topic: The seed keyword or topic to research.
        
    Returns:
        A dictionary containing main keyword data, related keywords, and proof keywords.
    """
    client = GoogleAdsClient()
    return client.get_keyword_ideas(topic)

def search_serp(query: str, location: str) -> Dict[str, Any]:
    """
    Performs a Google Search using SerpAPI to find organic results and related searches.
    
    Args:
        query: The search query.
        location: The location for the search (e.g., "Germany").
        
    Returns:
        A dictionary containing organic results, related searches, and people also ask.
    """
    client = SerpApiClient()
    return client.search(query, location=location)

def custom_search(query: str, num: int) -> Dict[str, Any]:
    """
    Performs a Google Custom Search to find relevant webpages.
    
    Args:
        query: The search query.
        num: Number of results to return.
        
    Returns:
        A dictionary containing search items.
    """
    client = CustomSearchClient()
    return client.search(query, num=num)

keyword_tool = FunctionTool(get_keyword_ideas)
serp_tool = FunctionTool(search_serp)
custom_search_tool = FunctionTool(custom_search)
