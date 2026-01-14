# GenSEO Agent Workshop

Welcome to the **GenSEO Agent Workshop**! In this workshop, you will build a full-stack AI application that automates SEO content creation using Google's Agent Development Kit (ADK), Gemini models, and a modern web stack.

## 🚀 Project Overview

We are building an **SEO Agent** that:

1.  **Researches** a topic using Google Ads, Google Search, and SerpAPI.
2.  **Analyzes** top-ranking competitors using Semantic Analysis (Gemini).
3.  **Generates** a comprehensive content briefing and draft.
4.  **Evaluates** its own work using a separate Evaluation Agent.

The application consists of three main components:

- **Agent (`/agent`)**: The core logic built with Python and ADK.
- **Backend (`/backend`)**: A FastAPI server that exposes the agent via a streaming API.
- **Frontend (`/frontend`)**: A Next.js web interface for real-time interaction.

## 📋 Prerequisites

Before you start, ensure you have the following installed:

- **Python 3.11+** (We recommend using `uv` for package management)
- **Node.js 18+** (and `npm`)
- **Google Cloud Project** with Vertex AI API enabled.
- **API Keys**:
  - `GOOGLE_API_KEY` (Gemini)
  - `SERPAPI_API_KEY` (Search results)
  - `GOOGLE_ADS_DEVELOPER_TOKEN` (Keyword research - optional but recommended)
  - `GOOGLE_SEARCH_API_KEY` & `GOOGLE_SEARCH_ENGINE_ID` (Custom Search)

## 🛠️ Quick Start

### 1. Environment Setup

Create a `.env` file in the root directory (see `.env.example`):

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 2. Install & Run Agent/Backend

We use `uv` for fast Python package management.

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to agent directory to sync environment
cd agent
uv sync

# Run the Backend (which imports the Agent)
# This runs on http://localhost:8000
PYTHONPATH=.. uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Install & Run Frontend

Open a new terminal for the frontend.

```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

### 4. Use the App

Open [http://localhost:3000](http://localhost:3000) in your browser.

1.  Enter a **Topic** (e.g., "Sustainable Coffee Brands").
2.  Select **Content Type** and **Target Group**.
3.  Click **Start Mission**.
4.  Watch the agent research, analyze, and write in real-time!

## 📂 Directory Structure

- `agent/`: Core AI agent code (ADK, Tools, Gemini integration).
- `backend/`: FastAPI application and SSE streaming logic.
- `frontend/`: Next.js React application with Tailwind CSS.
- `artifacts/`: Generated outputs (briefings, reports).

## 📚 Documentation

For detailed instructions on each component, check their respective READMEs:

- [Agent Documentation](./agent/README.md)
- [Backend Documentation](./backend/README.md)
- [Frontend Documentation](./frontend/README.md)
