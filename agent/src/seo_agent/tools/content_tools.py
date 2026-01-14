from typing import Dict, Any, List
from google.adk.tools import FunctionTool
from tools.jina_reader import JinaReaderClient

def parse_content(url: str) -> Dict[str, Any]:
    """
    Parses the content of a webpage using Jina Reader.
    
    Args:
        url: The URL of the webpage to parse.
        
    Returns:
        A dictionary containing the parsed content, title, and word count.
    """
    client = JinaReaderClient()
    return client.parse(url)

parsing_tool = FunctionTool(parse_content)
