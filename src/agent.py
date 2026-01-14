import asyncio
import os
import json
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

from google.adk import Agent as AdkAgent

from src.tools.google_ads import GoogleAdsClient
from src.tools.serp_api import SerpApiClient
from src.tools.custom_search import CustomSearchClient
from src.tools.jina_reader import JinaReaderClient
from src.tools.semantic_analysis import SemanticAnalysisClient
from src.tools.content_briefing import ContentBriefingClient
from src.tools.evaluation import EvaluationClient
from src.config import settings

# Load .env
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

from pydantic import PrivateAttr

class SEOAgent(AdkAgent):
    """
    SEO Agent using Google ADK.
    """
    _ads_client: GoogleAdsClient = PrivateAttr()
    _serp_client: SerpApiClient = PrivateAttr()
    _custom_search_client: CustomSearchClient = PrivateAttr()
    _jina_client: JinaReaderClient = PrivateAttr()
    _semantic_client: SemanticAnalysisClient = PrivateAttr()
    _briefing_client: ContentBriefingClient = PrivateAttr()
    _eval_client: EvaluationClient = PrivateAttr()

    def __init__(self):
        super().__init__(name="SEO_Agent")
        print("Initializing ADK SEO Agent...")
        self._ads_client = GoogleAdsClient()
        self._serp_client = SerpApiClient()
        self._custom_search_client = CustomSearchClient()
        self._jina_client = JinaReaderClient()
        self._semantic_client = SemanticAnalysisClient()
        self._briefing_client = ContentBriefingClient()
        self._eval_client = EvaluationClient()

    async def execute_mission(self, topic: str, content_type: str = "Landingpage", target_group: str = "General Audience", location: str = settings.DEFAULT_LOCATION, language: str = settings.DEFAULT_LANGUAGE):
        """
        Executes the SEO mission and yields events for streaming.
        """
        yield {"type": "status", "step": "init", "message": f"Starting mission for '{topic}'..."}
        
        report = {
            "topic": topic,
            "content_type": content_type,
            "target_group": target_group,
            "location": location,
            "language": language,
            "keyword_data": {},
            "competitors": [],
            "related_searches": [],
            "semantic_analysis": {},
            "briefing": "",
            "evaluation": ""
        }

        # Step 1: Parallel Execution
        yield {"type": "status", "step": "research", "message": "Running Keywords, SerpAPI & Custom Search in Parallel..."}
        
        kw_task = asyncio.to_thread(self._ads_client.get_keyword_ideas, topic)
        serp_task = asyncio.to_thread(self._serp_client.search, topic, location=location)
        custom_search_task = asyncio.to_thread(self._custom_search_client.search, topic, num=settings.MAX_COMPETITORS)
        
        kw_data, serp_data, custom_data = await asyncio.gather(kw_task, serp_task, custom_search_task)
        
        # Process Keywords
        if "error" in kw_data:
            report["keyword_data"] = {"error": kw_data['error']}
            yield {"type": "error", "source": "google_ads", "message": kw_data['error']}
        else:
            report["keyword_data"] = kw_data
            keywords = kw_data.get('related_keywords', [])
            kw_texts = [k if isinstance(k, str) else str(k) for k in keywords]
            yield {"type": "data", "key": "keywords", "data": kw_texts[:10]}
            yield {"type": "log", "message": f"Found {len(keywords)} keywords. Top 5: {', '.join(kw_texts[:5])}..."}

        # Process Competitors
        unique_links = set()
        merged_competitors = []
        related_searches = []

        # SerpAPI
        if "error" in serp_data:
            yield {"type": "error", "source": "serp_api", "message": serp_data['error']}
        else:
            organic = serp_data.get("organic_results", [])
            for item in organic:
                link = item.get("link")
                if link and link not in unique_links:
                    unique_links.add(link)
                    merged_competitors.append({"title": item.get("title"), "link": link, "source": "SerpAPI"})
            
            if "related_searches" in serp_data:
                related_searches = [item.get("query") for item in serp_data["related_searches"] if item.get("query")]
            elif "people_also_ask" in serp_data:
                 related_searches.extend([item.get("question") for item in serp_data["people_also_ask"] if item.get("question")])

        # Custom Search
        if "error" in custom_data:
            yield {"type": "error", "source": "custom_search", "message": custom_data['error']}
        else:
            items = custom_data.get("items", [])
            for item in items:
                link = item.get("link")
                if link and link not in unique_links:
                    unique_links.add(link)
                    merged_competitors.append({"title": item.get("title"), "link": link, "source": "CustomSearch"})

        top_competitors = merged_competitors[:settings.MAX_COMPETITORS]
        report["related_searches"] = related_searches
        
        yield {"type": "data", "key": "competitors", "data": top_competitors}
        yield {"type": "log", "message": f"Found {len(top_competitors)} competitors and {len(related_searches)} related searches."}

        # Step 2: Parsing
        yield {"type": "status", "step": "parsing", "message": f"Parsing {len(top_competitors)} URLs..."}
        
        parse_tasks = []
        for comp in top_competitors:
            parse_tasks.append(asyncio.to_thread(self._jina_client.parse, comp['link']))
        
        parsed_results = await asyncio.gather(*parse_tasks, return_exceptions=True)
        
        analyzed_content = []
        for i, res in enumerate(parsed_results):
            url = top_competitors[i]['link']
            if isinstance(res, Exception):
                yield {"type": "log", "message": f"[FAIL] {url}: {str(res)}"}
            elif res.get("word_count", 0) > 50:
                yield {"type": "log", "message": f"[OK] {url} ({res.get('word_count')} words)"}
                analyzed_content.append(res)
                report["competitors"].append({
                    "title": top_competitors[i].get("title"),
                    "link": url,
                    "word_count": res.get("word_count"),
                    "source": top_competitors[i].get("source")
                })
            else:
                yield {"type": "log", "message": f"[SKIP] {url} (Low content)"}

        # Step 3: Semantic Analysis
        if analyzed_content:
            yield {"type": "status", "step": "analysis", "message": "Running Semantic Analysis..."}
            context_keyword = f"{topic} (Type: {content_type}, Target: {target_group}, Related: {', '.join(related_searches[:5])})"
            
            report["semantic_analysis"] = await asyncio.to_thread(
                self._semantic_client.analyze, analyzed_content, context_keyword, language=language
            )
            yield {"type": "data", "key": "semantic_analysis", "data": report["semantic_analysis"]}
            
            # Step 4: Briefing
            yield {"type": "status", "step": "briefing", "message": "Generating Content Briefing..."}
            report["briefing"] = await asyncio.to_thread(
                self._briefing_client.generate_briefing, report, language=language
            )
            yield {"type": "data", "key": "briefing", "data": report["briefing"]}
            
            # Step 5: Evaluation
            yield {"type": "status", "step": "evaluation", "message": "Evaluating Briefing..."}
            report["evaluation"] = await asyncio.to_thread(
                self._eval_client.evaluate, report["briefing"], report
            )
            yield {"type": "data", "key": "evaluation", "data": report["evaluation"]}

        yield {"type": "complete", "report": report}

if __name__ == "__main__":
    agent = SEOAgent()
    # Run async main
    result = asyncio.run(agent.execute_mission("Familienhotel Mallorca", language="German"))
    
    # Save report
    with open("final_report_adk.json", "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    # Save briefing
    if result.get("briefing"):
        with open("briefing_adk.md", "w") as f:
            f.write(result["briefing"])
            
    # Save evaluation
    if result.get("evaluation"):
        with open("evaluation_adk.md", "w") as f:
            f.write(result["evaluation"])
            
    print("\nSaved: final_report_adk.json, briefing_adk.md, evaluation_adk.md")
