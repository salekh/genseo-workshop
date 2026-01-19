# GenSEO Agent with Agent Development Kit (ADK)

This directory contains the source code for the GenSEO Agent, built using the **Google Agent Development Kit (ADK)**. The agent is designed to autonomously research topics, analyze competitors, and generate SEO-optimized content briefings.

## 🧠 Agent Overview

The GenSEO Agent follows a **multi-agent architecture** (or a sequential workflow) to handle complex SEO tasks. It leverages **Google Gemini** models for reasoning and content generation, and integrates with external tools like Google Ads and SerpAPI for real-time data.

### Design Pattern

The agent is structured as a **Sequential Agent** (or a coordinated workflow of sub-agents/tools):

1.  **Researcher**: Gathers keyword data (Google Ads) and search results (SerpAPI, Custom Search).
2.  **Content Parser**: Scrapes and extracts relevant content from competitor URLs (Jina Reader).
3.  **Semantic Analyzer**: Uses Gemini to analyze competitor content and identify content gaps/opportunities.
4.  **Briefing Generator**: Synthesizes all data into a comprehensive content briefing.
5.  **Evaluator**: Critiques the generated briefing for quality and completeness.

## 🚀 Initialization & Setup

Ensure you have the necessary environment variables set in the root `.env` file (see `.env.example`).

### Prerequisites

- Python 3.13+
- `uv` (recommended) or `pip`
- Google Cloud Project with Vertex AI enabled

### Installation

Navigate to the `agent` directory and install dependencies:

```bash
cd agent
uv sync
```

## 🧪 Testing with ADK Web

The ADK provides a built-in web interface for testing and interacting with your agent in a chat-like environment. This is useful for debugging and verifying agent behavior before integrating it with the full backend/frontend.

To start the ADK test environment:

```bash
# From agent/src directory
adk web --port 8001
```

Once running, open your browser at [http://localhost:8001](http://localhost:8001). You can interact with the agent directly, simulating user requests (e.g., "Create a briefing for 'Sustainable Coffee'").

## 📂 Directory Structure

- **`agent.py`**: Main entry point defining the `SEOAgent` class.
- **`config.py`**: Configuration settings and environment variable loading.
- **`tools/`**: Implementation of individual tools (Google Ads, SerpAPI, etc.).
- **`seo_agent/`**: (Optional/Advanced) Contains sub-agent definitions if using a decomposed architecture.

## 🔧 Key Components

- **`GoogleAdsClient`**: Fetches keyword search volume and competition data.
- **`SerpApiClient`**: Retrieves top ranking organic results.
- **`JinaReaderClient`**: Converts web pages to LLM-friendly markdown.
- **`SemanticAnalysisClient`**: Uses Gemini to perform deep content analysis.
