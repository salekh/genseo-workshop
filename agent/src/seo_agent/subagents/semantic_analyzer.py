import asyncio
from typing import Dict, Any, List
from google.adk import Agent
from ..tools.analysis_tools import semantic_tool
from config import settings

class SemanticAnalyzer(Agent):
    """
    Agent responsible for semantic analysis of content.
    """
    def __init__(self):
        super().__init__(
            name="SemanticAnalyzer",
            model="gemini-3-pro-preview",
            description="Analyzes content semantically to identify entities, gaps, and opportunities.",
            instruction="You are a semantic analysis expert. Analyze the provided content to find SEO opportunities.",
            tools=[semantic_tool],
            output_key="semantic_analysis"
        )

    async def analyze(self, analyzed_content: List[Dict[str, Any]], topic: str, content_type: str, target_group: str, related_searches: List[str], language: str = settings.DEFAULT_LANGUAGE) -> Dict[str, Any]:
        """
        Performs semantic analysis on the parsed content.
        """
        context_keyword = f"{topic} (Type: {content_type}, Target: {target_group}, Related: {', '.join(related_searches[:5])})"
        
        analysis_result = await asyncio.to_thread(
            semantic_tool.func, analyzed_content, context_keyword, language=language
        )
        
        return {
            "semantic_analysis": analysis_result,
            "logs": [
                {"type": "data", "key": "semantic_analysis", "data": analysis_result}
            ]
        }
