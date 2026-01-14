import os
import json
from typing import Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient as LibGoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Load .env - adjusted to check current directory or parents
load_dotenv()

class GoogleAdsClient:
    """
    A wrapper around the Google Ads Python Client Library (v22).
    """
    def __init__(self):
        # Configuration mapping
        self.config = {
            "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
            "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
            "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
            "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
            "use_proto_plus": True
        }

        # Target Account (Client Account ID)
        self.customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID", self.config["login_customer_id"])

        if not all([self.config[k] for k in ["developer_token", "client_id", "client_secret", "refresh_token"]]):
            raise ValueError("Missing Google Ads configuration in .env. Check DEVELOPER_TOKEN, CLIENT_ID, etc.")

        try:
            # Force v22 to ensure 2026 compatibility
            self.client = LibGoogleAdsClient.load_from_dict(self.config, version="v22")
        except Exception as e:
            print(f"Failed to initialize Google Ads Client: {e}")
            raise

    def get_keyword_ideas(self, keyword: str, location_id: str = "2276", language_id: str = "1001") -> Dict[str, Any]:
        keyword_plan_idea_service = self.client.get_service("KeywordPlanIdeaService")
        customer_id_clean = self.customer_id.replace("-", "")
        
        request = self.client.get_type("GenerateKeywordIdeasRequest")
        request.customer_id = customer_id_clean
        
        # Resource Paths for v22
        request.language = f"languageConstants/{language_id}"
        request.geo_target_constants.append(f"geoTargetConstants/{location_id}")
        
        request.include_adult_keywords = False
        request.keyword_plan_network = self.client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
        request.keyword_seed.keywords.append(keyword)
        
        # Add Concept annotations for categorized results
        request.keyword_annotation.append(
            self.client.enums.KeywordPlanKeywordAnnotationEnum.KEYWORD_CONCEPT
        )

        try:
            response = keyword_plan_idea_service.generate_keyword_ideas(request=request)
            return self._process_results(response, keyword)
        except GoogleAdsException as ex:
            print(f"Request {ex.request_id} failed. Status: {ex.error.code().name}")
            for error in ex.failure.errors:
                print(f"\tDetail: {error.message}")
            return {"error": ex.failure.errors[0].message}

    def _process_results(self, response, seed_keyword: str) -> Dict[str, Any]:
        main_keyword_data = None
        related_keywords = []
        word_counts = {}
        
        for result in response:
            text = result.text
            metrics = result.keyword_idea_metrics
            
            # Robust extraction of metrics
            avg_searches = getattr(metrics, 'avg_monthly_searches', 0)
            comp_enum = getattr(metrics, 'competition', None)
            competition = comp_enum.name if comp_enum else "UNKNOWN"
            
            item = {
                "keyword": text,
                "avg_searches": avg_searches,
                "competition": competition
            }
            
            if text.lower() == seed_keyword.lower():
                main_keyword_data = item
            else:
                related_keywords.append(item)
                
            # Proof-keyword extraction logic
            for word in text.split():
                clean_word = word.lower().strip(".,!?")
                if len(clean_word) > 3 and clean_word not in seed_keyword.lower():
                    word_counts[clean_word] = word_counts.get(clean_word, 0) + 1

        # Sorting
        related_keywords.sort(key=lambda x: x["avg_searches"] or 0, reverse=True)
        sorted_proof = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        proof_keywords = [word for word, count in sorted_proof[:8]]

        return {
            "main_keyword": main_keyword_data,
            "related_keywords": related_keywords[:10],
            "proof_keywords": proof_keywords
        }

# --- TEST FUNCTION ---
if __name__ == "__main__":
    print("--- Starting Google Ads Keyword Analysis ---")
    try:
        # Initialize Wrapper
        ads_wrapper = GoogleAdsClient()
        
        # Run Query
        search_query = "familienhotel mallorca"
        print(f"Analyzing: {search_query}...")
        
        # Defaulting to Germany (2276) and German (1001)
        result_data = ads_wrapper.get_keyword_ideas(search_query)

        if "error" in result_data:
            print(f"FAILED: {result_data['error']}")
        else:
            print("\n" + "="*40)
            print("SEO ANALYSIS RESULTS")
            print("="*40)
            
            # 1. Main Keyword
            main = result_data.get("main_keyword")
            if main:
                print(f"Target: \"{main['keyword']}\"")
                print(f"Volume: {main['avg_searches']} searches/mo")
                print(f"Competition: {main['competition']}")
            
            # 2. Related Keywords
            print("\nTop 10 Related Terms:")
            for kw in result_data.get("related_keywords", []):
                print(f" • {kw['keyword']:<30} | Vol: {kw['avg_searches']}")

            # 3. Content Proof Keywords
            print("\nContent 'Proof' Keywords (Semantic Gap):")
            print(f" {', '.join(result_data.get('proof_keywords', []))}")
            print("="*40)

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")