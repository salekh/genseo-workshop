import asyncio
from typing import Dict, Any, List
from google.adk import Agent
from ..tools.analysis_tools import briefing_tool
from ...config import settings
from ..models import ReportData, BriefingGeneratorResult

class BriefingGenerator(Agent):
    """
    Agent responsible for generating the content briefing.
    """
    def __init__(self):
        super().__init__(
            name="BriefingGenerator",
            model="gemini-2.5-pro",
            description="Generates a comprehensive content briefing based on research and analysis. Can also improve briefings based on feedback.",
            instruction="You are a content strategist. Create a detailed content brief based on the provided research. If provided with recommendations and an original briefing, use them to IMPROVE the briefing.",
            tools=[briefing_tool],
            output_key="briefing"
        )

    async def generate(self, report: ReportData, language: str = settings.DEFAULT_LANGUAGE) -> BriefingGeneratorResult:
        """
        Generates the content briefing.
        """
        briefing = await asyncio.to_thread(
            briefing_tool.func, report.model_dump(), language=language
        )
        
        return BriefingGeneratorResult(
            briefing=briefing,
            logs=[
                {"type": "data", "key": "briefing", "data": briefing}
            ]
        )
