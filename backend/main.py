import asyncio
import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel

# Import Agent (adjust path if needed, or better, install agent as a package)
# For now, we'll append the agent directory to sys.path
import sys
from pathlib import Path
# Current file is in backend/main.py
# We want to import from agent/src/agent.py
# So we need to add 'agent' folder to sys.path if we want 'from src.agent import ...'
# OR add 'agent/src' to sys.path if we want 'from agent import ...'
# The agent code uses 'from src.tools...' so it expects 'src' to be a package or in path?
# Let's check agent/src/agent.py imports.
# It uses 'from src.tools...'
# So we need the parent of 'src' (which is 'agent') to be in sys.path?
# No, if we run from 'agent' dir, 'src' is a package.
# Let's add 'agent' to sys.path.
agent_path = Path(__file__).resolve().parents[1] / 'agent'
sys.path.append(str(agent_path))

from src.agent import SEOAgent
from src.config import settings

app = FastAPI(title="GenSEO Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = SEOAgent()

class MissionRequest(BaseModel):
    topic: str
    content_type: str = "Landingpage"
    target_group: str = "General Audience"
    location: str = "Germany"
    language: str = "German"

@app.get("/api/mission/stream")
async def stream_mission(
    topic: str = Query(..., description="Main Keyword/Topic"),
    content_type: str = Query("Landingpage", description="Type of content"),
    target_group: str = Query("General Audience", description="Target Audience"),
    location: str = Query("Germany", description="Target Region"),
    language: str = Query("German", description="Language")
):
    """
    Streams the SEO mission execution events.
    """
    async def event_generator():
        async for event in agent.execute_mission(
            topic=topic,
            content_type=content_type,
            target_group=target_group,
            location=location,
            language=language
        ):
            # SSE format: data: <json>\n\n
            yield {"data": json.dumps(event)}

    return EventSourceResponse(event_generator())

@app.get("/health")
def health_check():
    return {"status": "ok"}
