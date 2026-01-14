import asyncio
from typing import Dict, Any, List
from google.adk import Agent
from ..tools.analysis_tools import evaluation_tool
from ..models import ReportData, BriefingEvaluatorResult

class BriefingEvaluator(Agent):
    """
    Agent responsible for evaluating the content briefing.
    """
    def __init__(self):
        super().__init__(
            name="BriefingEvaluator",
            model="gemini-2.5-pro",
            description="Evaluates the content briefing against best practices and requirements.",
            instruction="You are a senior editor. Evaluate the content brief for quality and completeness.",
            tools=[evaluation_tool]
        )

    async def evaluate(self, briefing: str, report: ReportData) -> BriefingEvaluatorResult:
        """
        Evaluates the content briefing.
        """
        evaluation = await asyncio.to_thread(
            evaluation_tool.func, briefing, report.model_dump()
        )
        
        return BriefingEvaluatorResult(
            evaluation=evaluation,
            logs=[
                {"type": "data", "key": "evaluation", "data": evaluation}
            ]
        )
