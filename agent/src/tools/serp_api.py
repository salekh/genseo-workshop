import os
import requests
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).resolve().parents[3] / '.env'
load_dotenv(dotenv_path=env_path)

class SerpApiClient:
    """
    A light wrapper around the SerpAPI Google Search Engine.
    """
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")
        self.base_url = "https://serpapi.com/search"

        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY environment variable not set")

    def search(self, query: str, location: str = "Germany", hl: str = "de", gl: str = "de") -> Dict[str, Any]:
        """
        Perform a search using SerpAPI.

        Args:
            query: The search term.
            location: The location to restrict results to (e.g., 'Germany').
            hl: The language code (e.g., 'de').
            gl: The country code (e.g., 'de').

        Returns:
            The JSON response from SerpAPI.
        """
        params = {
            "engine": "google",
            "q": query,
            "location": location,
            "hl": hl,
            "gl": gl,
            "api_key": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching SerpAPI results: {e}")
            if response is not None:
                print(f"Response: {response.text}")
            return {"error": str(e)}

if __name__ == "__main__":
    import json
    try:
        client = SerpApiClient()
        # Test with "Familienhotel Mallorca"
        print("Searching for 'Familienhotel Mallorca'...")
        results = client.search("Familienhotel Mallorca")
        
        if "error" in results:
            print(f"Error: {results['error']}")
        else:
            print(json.dumps(results, indent=2, ensure_ascii=False))
                
    except Exception as e:
        print(f"Failed: {e}")
