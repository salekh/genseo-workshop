import os
import json
from typing import List, Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path(__file__).resolve().parents[3] / '.env'
load_dotenv(dotenv_path=env_path)

class SemanticAnalysisClient:
    """
    A client for performing semantic analysis on competitor content using Gemini.
    """
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.project_id = os.getenv("PROJECT_ID")
        self.location = os.getenv("LOCATION")

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        elif self.project_id and self.location:
            self.client = genai.Client(vertexai=True, project=self.project_id, location=self.location)
        else:
            raise ValueError("Either GOOGLE_API_KEY or PROJECT_ID/LOCATION must be set")
        self.model = "gemini-2.5-pro"

    def analyze(self, competitor_contents: List[Dict[str, Any]], keyword: str, language: str = "German") -> Dict[str, Any]:
        """
        Analyzes competitor content to extract entities, topics, and content gaps.

        Args:
            competitor_contents: List of dictionaries with 'title' and 'main_content'.
            keyword: The target keyword.
            language: The language for the output analysis (default: "German").

        Returns:
            Structured dictionary with analysis results.
        """
        
        # Prepare context from competitor articles
        articles_text = ""
        for i, article in enumerate(competitor_contents, 1):
            title = article.get("title", "Unknown Title")
            content = article.get("main_content", "")[:5000] # Truncate to avoid huge context if needed, though Gemini 2.0 has large context
            articles_text += f"\n--- ARTICLE {i}: {title} ---\n{content}\n"

        prompt = f"""
        You are an SEO Expert. Perform a semantic analysis for the keyword "{keyword}" based on the following competitor articles.
        
        COMPETITOR CONTENT:
        {articles_text}
        
        TASK:
        Analyze the text to extract:
        1. Frequent Entities (Places, Hotels, Concepts).
        2. Topic Clusters (What topics are covered? How many articles cover them?).
        3. Content Gaps (What is missing or under-represented?).

        IMPORTANT: Generate the analysis in {language}.

        OUTPUT FORMAT (JSON):
        {{
            "keyword": "{keyword}",
            "entities": {{
                "places": ["Place 1", "Place 2"],
                "hotels": ["Hotel 1", "Hotel 2"],
                "concepts": ["Concept 1", "Concept 2"]
            }},
            "topic_clusters": [
                {{"topic": "Topic Name", "coverage": "X/Y articles", "status": "High/Medium/Low"}}
            ],
            "content_gaps": [
                "Gap 1",
                "Gap 2"
            ]
        }}
        
        Return ONLY valid JSON.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                return json.loads(response.text)
            else:
                return {"error": "Empty response from Gemini"}

        except Exception as e:
            print(f"Error during semantic analysis: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    # Test with dummy data
    client = SemanticAnalysisClient()
    
    dummy_content = [
        {
            "title": "Top 10 Familienhotels Mallorca",
            "main_content": "Das Viva Blue in Alcudia ist toll. Es gibt Wasserrutschen und All-Inclusive. Der Strand ist nah."
        },
        {
            "title": "Kinderhotels auf Mallorca",
            "main_content": "Wir empfehlen das Zafiro Palace in Alcudia. Super Kinderclub und Pools. All-Inclusive ist verfügbar."
        }
    ]
    
    print("Running Semantic Analysis (in English)...")
    try:
        result = client.analyze(dummy_content, "Familienhotel Mallorca", language="English")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Failed: {e}")
