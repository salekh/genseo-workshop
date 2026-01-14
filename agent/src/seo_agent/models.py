from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, List

class ReportData(BaseModel):
    model_config = ConfigDict(extra='ignore')  # Allow other keys from the report

    topic: str
    keyword_data: Dict[str, Any]
    competitors: List[Dict[str, Any]]
    related_searches: List[str]
    parsed_content: List[Dict[str, Any]] = []
    semantic_analysis: Dict[str, Any] = {}
    briefing: str = ""
    evaluation: str = ""

class BriefingGeneratorResult(BaseModel):
    briefing: str
    logs: List[Dict[str, Any]]

class BriefingEvaluatorResult(BaseModel):
    evaluation: str
    logs: List[Dict[str, Any]]
