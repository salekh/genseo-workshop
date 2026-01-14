import asyncio
import uuid
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import SequentialAgent
from google.genai import types
from config import settings
from .subagents.briefing_evaluator import BriefingEvaluator
from .subagents.briefing_generator import BriefingGenerator
from .subagents.content_parser import ContentParser
from .subagents.researcher import Researcher
from .subagents.semantic_analyzer import SemanticAnalyzer

# Load .env 
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

# Instantiate subagents
researcher_agent = Researcher()
parser_agent = ContentParser()
analyzer_agent = SemanticAnalyzer()
briefing_generator_agent = BriefingGenerator()

root_agent = SequentialAgent(
    name="SEO_Root_Agent",
    description="An autonomous agent that researches topics, analyzes competitors, and generates SEO content briefings.",
    sub_agents=[
        researcher_agent,
        parser_agent,
        analyzer_agent,
        briefing_generator_agent,
    ],
)