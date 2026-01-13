import requests
import re
from typing import Dict, Any, Optional

class JinaReaderClient:
    """
    A client for Jina Reader API (https://jina.ai/reader) to parse webpages.
    """
    def __init__(self):
        self.base_url = "https://r.jina.ai/"

    def parse(self, url: str) -> Dict[str, Any]:
        """
        Parses a webpage using Jina Reader.

        Args:
            url: The URL of the webpage to parse.

        Returns:
            A dictionary containing:
            - url: The original URL
            - title: The title of the page (extracted if possible)
            - word_count: The word count of the main content
            - main_content: The extracted main content
        """
        target_url = f"{self.base_url}{url}"
        
        # Jina Reader allows some configuration via headers
        headers = {
            "X-Retain-Images": "none",
            "Accept": "application/json" 
        }

        try:
            response = requests.get(target_url, headers=headers)
            response.raise_for_status()
            
            # Try to parse as JSON if Jina returns JSON
            try:
                response_data = response.json()
                
                # Jina's JSON format puts content in a 'data' field
                data = response_data.get("data", {})
                
                if not data:
                    # Fallback if 'data' is missing but maybe root has it (unlikely based on debug)
                    data = response_data
                
                title = data.get("title", "No Title Found")
                content = data.get("content", "")
                url_returned = data.get("url", url)
                
                # Calculate word count
                word_count = len(content.split())
                
                return {
                    "url": url_returned,
                    "title": title,
                    "word_count": word_count,
                    "main_content": content
                }
            except ValueError:
                print(f"DEBUG: Response was not JSON. First 100 chars: {response.text[:100]}")
                # Fallback if response is plain text/markdown (older Jina behavior or if JSON fails)
                content = response.text
                
                # Simple extraction attempt for title from markdown (e.g. # Title)
                title = "No Title Found"
                lines = content.split('\n')
                if lines and lines[0].startswith('# '):
                    title = lines[0][2:].strip()
                
                word_count = len(content.split())
                
                return {
                    "url": url,
                    "title": title,
                    "word_count": word_count,
                    "main_content": content
                }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching Jina Reader results: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    import json
    client = JinaReaderClient()
    # Test with the user provided URL
    test_url = "https://www.tui.com/kinderhotels/mallorca"
    print(f"Parsing {test_url}...")
    result = client.parse(test_url)
    print(f"Title: {result.get('title')}")
    print(f"Word Count: {result.get('word_count')}")
    # print(json.dumps(result, indent=2, ensure_ascii=False))
