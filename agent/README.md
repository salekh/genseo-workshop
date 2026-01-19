# GenSEO Agent (Python/ADK)

The **GenSEO Agent** is the brain of the operation. Built using the **Google Agent Development Kit (ADK)**, it orchestrates the SEO workflow.

## 🧠 Capabilities

The agent performs the following steps in parallel/sequence:
1.  **Keyword Research**: Uses Google Ads API to find search volume and competition.
2.  **Competitor Discovery**: Uses SerpAPI and Google Custom Search to find top-ranking pages.
3.  **Content Parsing**: Uses `jina-reader` to extract clean text from competitor URLs.
4.  **Semantic Analysis**: Uses Gemini to analyze competitor content, identify gaps, and extract entities.
5.  **Content Briefing**: Generates a detailed content brief and draft using Gemini.
6.  **Evaluation**: A separate "Critic" agent evaluates the draft against SEO best practices.

## ⚙️ Configuration

The agent is configured via `src/config.py` and environment variables.

### Key Settings (`src/config.py`)
-   `MAX_COMPETITORS`: Number of competitor URLs to analyze (Default: 10).
-   `DEFAULT_LOCATION`: Default target region (Default: "Germany").
-   `DEFAULT_LANGUAGE`: Default language (Default: "German").

### Environment Variables (`.env`)
Ensure these are set in your root `.env` file:
-   `GOOGLE_API_KEY`: For Gemini models.
-   `SERPAPI_API_KEY`: For Google Search results.
-   `GOOGLE_SEARCH_API_KEY`: For Custom Search.
-   `GOOGLE_SEARCH_ENGINE_ID`: For Custom Search.
-   `GOOGLE_ADS_*`: For Google Ads API (optional).

## 🛠️ Development

### Setup
First, clone the repository:
```bash
git clone https://github.com/sanchitalekh/genseo-workshop.git
cd genseo-workshop/agent
```

### Dependencies
We use `uv` for dependency management.

First, install `uv` if you haven't already:
```bash
pip install uv
```

Then, install the project dependencies:
```bash
uv sync
```

### Project Structure
-   `src/agent.py`: Main `SEOAgent` class.
-   `src/tools/`: Individual tool implementations.
    -   `custom_search.py`: Google Custom Search wrapper.
    -   `serp_api.py`: SerpAPI wrapper.
    -   `jina_reader.py`: Content scraper.
    -   `semantic_analysis.py`: Gemini-based analysis.
    -   `content_briefing.py`: Gemini-based writing.
    -   `evaluation.py`: Gemini-based critique.

### Running Standalone
You can run the agent logic directly for testing purposes. This runs the application in a local server, including the backend as well as the frontend.

```bash
./start_app.sh
```

### Running with ADK Web UI
You can run the agent independently using the built-in ADK Web UI:

1.  **Ensure the `src` directory is recognized**:
    (This has been initialized with `touch agent/src/__init__.py` and `root_agent` exposure in `agent.py`)

2.  **Launch the ADKWeb UI**:
    From the `agent/` directory:
    ```bash
    PYTHONPATH=. uv run adk web . --port 8001
    ```

3.  **Access the UI**:
    Open [http://localhost:8001](http://localhost:8001) in your browser. Select the **src** agent to start interacting.
