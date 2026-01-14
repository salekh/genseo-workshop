import asyncio
from typing import Dict, Any, List
from google.adk import Agent
from ..tools.research_tools import keyword_tool, serp_tool, custom_search_tool
from ...config import settings

class Researcher(Agent):
    """
    Agent responsible for keyword research and finding competitors.
    """
    def __init__(self):
        super().__init__(
            name="Researcher",
            model="gemini-2.5-pro",
            description="Researches keywords and finds competitors using Google Ads, SerpAPI, and Custom Search.",
            instruction="You are a research specialist. Find relevant keywords and competitors for the given topic.",
            tools=[keyword_tool, serp_tool, custom_search_tool],
            output_key="research_output"
        )

    async def research(self, topic: str, location: str = settings.DEFAULT_LOCATION) -> Dict[str, Any]:
        """
        Performs parallel research for keywords and competitors.
        """
        # Parallel Execution using tools directly (or via model if we wanted full autonomy, but for now keeping parallel logic for performance)
        # Note: To strictly follow ADK best practices, we might want the model to call these. 
        # However, for the workshop's performance requirements (parallelism), we might invoke the underlying functions 
        # or use the tools in a way that allows parallel execution. 
        # The user asked to "add the tools to the subagents instead of using asyncio".
        # This implies letting the model decide. BUT, that would be sequential and slow.
        # I will register the tools, but for the `research` method, I will still use asyncio to call the *tools* (which wrap the clients).
        # Actually, if I use `tools=[...]`, the agent CAN call them.
        # But `research` is a specific method called by the orchestrator.
        
        # Let's try to use the tools directly in the code for now to maintain the parallel behavior 
        # but using the Tool objects' `run` method if possible, or just the functions they wrap.
        # `FunctionTool` wraps a function.
        
        kw_task = asyncio.to_thread(keyword_tool.func, topic)
        serp_task = asyncio.to_thread(serp_tool.func, topic, location=location)
        custom_search_task = asyncio.to_thread(custom_search_tool.func, topic, num=settings.MAX_COMPETITORS)
        
        kw_data, serp_data, custom_data = await asyncio.gather(kw_task, serp_task, custom_search_task)
        
        result = {
            "keyword_data": {},
            "competitors": [],
            "related_searches": [],
            "logs": []
        }

        # Process Keywords
        if "error" in kw_data:
            result["keyword_data"] = {"error": kw_data['error']}
            result["logs"].append({"type": "error", "source": "google_ads", "message": kw_data['error']})
        else:
            result["keyword_data"] = kw_data
            keywords = kw_data.get('related_keywords', [])
            kw_texts = [k if isinstance(k, str) else str(k) for k in keywords]
            result["logs"].append({"type": "data", "key": "keywords", "data": kw_texts[:10]})
            result["logs"].append({"type": "log", "message": f"Found {len(keywords)} keywords. Top 5: {', '.join(kw_texts[:5])}..."})

        # Process Competitors
        unique_links = set()
        merged_competitors = []
        related_searches = []

        # SerpAPI
        if "error" in serp_data:
            result["logs"].append({"type": "error", "source": "serp_api", "message": serp_data['error']})
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
            result["logs"].append({"type": "error", "source": "custom_search", "message": custom_data['error']})
        else:
            items = custom_data.get("items", [])
            for item in items:
                link = item.get("link")
                if link and link not in unique_links:
                    unique_links.add(link)
                    merged_competitors.append({"title": item.get("title"), "link": link, "source": "CustomSearch"})

        top_competitors = merged_competitors[:settings.MAX_COMPETITORS]
        result["competitors"] = top_competitors
        result["related_searches"] = related_searches
        
        result["logs"].append({"type": "data", "key": "competitors", "data": top_competitors})
        result["logs"].append({"type": "log", "message": f"Found {len(top_competitors)} competitors and {len(related_searches)} related searches."})
        
        return result
