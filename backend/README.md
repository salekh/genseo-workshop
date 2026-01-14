# GenSEO Backend (FastAPI)

The **GenSEO Backend** is a lightweight FastAPI server that exposes the Agent's capabilities to the frontend via a streaming API.

## 🔌 API Endpoints

### `GET /api/mission/stream`

Streams the execution of an SEO mission using Server-Sent Events (SSE).

**Parameters:**

- `topic` (required): The main keyword or topic (e.g., "Vegan Leather Shoes").
- `content_type`: Type of content to generate (e.g., "Landingpage", "Blog Post").
- `target_group`: Target audience (e.g., "Eco-conscious consumers").
- `location`: Target region (e.g., "Germany").
- `language`: Output language (e.g., "German").

**Response:**
A stream of JSON events:

- `status`: Current step updates (e.g., "Parsing content...").
- `log`: Detailed logs (e.g., "Found 10 competitors").
- `data`: Intermediate results (e.g., generated briefing).
- `complete`: Final report.

## 🚀 Running the Server

The backend requires the `agent` module to be in the python path.

```bash
# From the root directory
cd backend

# Run with uvicorn (ensure PYTHONPATH includes the parent directory)
PYTHONPATH=.. uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start at `http://localhost:8000`.
Health check: `http://localhost:8000/health` (if implemented) or check docs at `http://localhost:8000/docs`.

## 📦 Dependencies

- `fastapi`
- `uvicorn`
- `sse-starlette`
- `pydantic-settings`
- `google-adk` (and other agent dependencies)
