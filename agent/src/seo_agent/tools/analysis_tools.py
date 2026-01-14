from typing import Dict, Any, List
from google.adk.tools import FunctionTool
from tools.semantic_analysis import SemanticAnalysisClient
from tools.content_briefing import ContentBriefingClient
from tools.evaluation import EvaluationClient
from config import settings
from seo_agent.models import ReportData

def analyze_semantics(analyzed_content: List[Dict[str, Any]], context: str, language: str = settings.DEFAULT_LANGUAGE) -> Dict[str, Any]:
    """
    Performs semantic analysis on parsed content to identify entities, gaps, and opportunities.
    
    Args:
        analyzed_content: List of parsed content dictionaries.
        context: Context string describing the topic and target.
        language: Language for the analysis.
        
    Returns:
        A dictionary containing semantic analysis results.
    """
    client = SemanticAnalysisClient()
    return client.analyze(analyzed_content, context, language=language)

def generate_briefing(report: Dict[str, Any], language: str = settings.DEFAULT_LANGUAGE) -> str:
    """
    Generates a comprehensive content briefing based on the research report.
    
    Args:
        report: The full research report containing keywords, competitors, and analysis.
        language: Language for the briefing.
        
    Returns:
        The generated briefing in Markdown format.
    """
    client = ContentBriefingClient()
    return client.generate_briefing(report, language=language)

def evaluate_briefing(briefing: str, report: Dict[str, Any]) -> str:
    """
    Evaluates a content briefing against best practices and the research report.
    
    Args:
        briefing: The content briefing to evaluate.
        report: The research report used to generate the briefing.
        
    Returns:
        The evaluation result in Markdown format.
    """
    client = EvaluationClient()
    return client.evaluate(briefing, report)

semantic_tool = FunctionTool(analyze_semantics)
briefing_tool = FunctionTool(generate_briefing)
evaluation_tool = FunctionTool(evaluate_briefing)
