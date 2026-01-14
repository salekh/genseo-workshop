import asyncio
from typing import Dict, Any, List
from google.adk import Agent
from ..tools.content_tools import parsing_tool

class ContentParser(Agent):
    """
    Agent responsible for parsing content from URLs.
    """
    def __init__(self):
        super().__init__(
            name="ContentParser",
            model="gemini-3-pro-preview",
            description="Parses content from URLs using Jina Reader.",
            instruction="You are a content extraction specialist. Extract readable content from the provided URLs.",
            tools=[parsing_tool],
            output_key="parsed_content"
        )

    async def parse(self, urls: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Parses content from a list of competitor URLs.
        """
        result = {
            "analyzed_content": [],
            "competitors_with_content": [],
            "logs": []
        }
        
        parse_tasks = []
        for comp in urls:
            parse_tasks.append(asyncio.to_thread(parsing_tool.func, comp['link']))
        
        parsed_results = await asyncio.gather(*parse_tasks, return_exceptions=True)
        
        for i, res in enumerate(parsed_results):
            url = urls[i]['link']
            if isinstance(res, Exception):
                result["logs"].append({"type": "log", "message": f"[FAIL] {url}: {str(res)}"})
            elif res.get("word_count", 0) > 50:
                result["logs"].append({"type": "log", "message": f"[OK] {url} ({res.get('word_count')} words)"})
                result["analyzed_content"].append(res)
                result["competitors_with_content"].append({
                    "title": urls[i].get("title"),
                    "link": url,
                    "word_count": res.get("word_count"),
                    "source": urls[i].get("source")
                })
            else:
                result["logs"].append({"type": "log", "message": f"[SKIP] {url} (Low content)"})
                
        return result
