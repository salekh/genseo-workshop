import os
import requests
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).resolve().parents[3] / '.env'
load_dotenv(dotenv_path=env_path)

class CustomSearchClient:
    """
    A light wrapper around the Google Custom Search JSON API.
    """
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.cx = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        self.base_url = "https://www.googleapis.com/customsearch/v1"

        if not self.api_key:
            raise ValueError("GOOGLE_SEARCH_API_KEY environment variable not set")
        if not self.cx:
            raise ValueError("GOOGLE_SEARCH_ENGINE_ID environment variable not set")

    def search(self, query: str, country: str = "de", language: str = "lang_de", num: int = 10) -> Dict[str, Any]:
        """
        Perform a search using the Google Custom Search API.

        Args:
            query: The search term.
            country: The country to restrict results to (e.g., 'de' for Germany).
            language: The language to restrict results to (e.g., 'lang_de' for German).
            num: Number of results to return. Note: API returns max 10 per request.
                 If num > 10, multiple requests will be made (up to 100 results max usually).

        Returns:
            A dictionary containing the combined results.
            'items' will contain the list of all found items.
            'searchInformation' will be from the last request (or aggregated).
        """
        all_items = []
        start_index = 1
        max_results_per_request = 10
        
        # Safety limit to prevent infinite loops or excessive quota usage
        max_allowed = 100 
        if num > max_allowed:
            num = max_allowed

        combined_response = {}

        while len(all_items) < num:
            # Calculate how many to fetch in this batch
            remaining = num - len(all_items)
            batch_num = min(remaining, max_results_per_request)

            params = {
                "key": self.api_key,
                "cx": self.cx,
                "q": query,
                "gl": country,
                "lr": language,
                "num": batch_num,
                "start": start_index
            }

            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if "items" in data:
                    all_items.extend(data["items"])
                
                # Keep the last response metadata, but update items
                combined_response = data
                combined_response["items"] = all_items

                # Check if we have reached the end of results
                if "items" not in data or len(data["items"]) < batch_num:
                    break
                
                # Prepare for next page
                start_index += len(data["items"])
                
            except requests.exceptions.RequestException as e:
                print(f"Error performing search at start_index {start_index}: {e}")
                if not combined_response:
                    return {"error": str(e)}
                break # Return what we have so far

        return combined_response

if __name__ == "__main__":
    # Example usage
    try:
        client = CustomSearchClient()
        # Requesting 15 results to test pagination
        results = client.search("Familienhotel Mallorca", country="de", num=15)
        
        if "items" in results:
            print(f"Found {len(results['items'])} results:")
            for i, item in enumerate(results["items"], 1):
                print(f"{i}. {item['title']} ({item['link']})")
        else:
            print("No results found or error occurred.")
            print(results)
    except Exception as e:
        print(f"Failed to initialize client: {e}")
