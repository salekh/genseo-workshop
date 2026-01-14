import os
from typing import Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path(__file__).resolve().parents[3] / '.env'
load_dotenv(dotenv_path=env_path)

class EvaluationClient:
    """
    A client for evaluating SEO Content Briefings using Gemini.
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

    def evaluate(self, briefing: str, report_data: Dict[str, Any]) -> str:
        """
        Evaluates the briefing against the SEO report data.

        Args:
            briefing: The generated markdown briefing.
            report_data: The original SEO report data.

        Returns:
            Markdown evaluation report.
        """
        
        prompt = f"""
        You are a Senior SEO Editor. Evaluate the following Content Briefing against the provided SEO Data.
        
        SEO DATA:
        {report_data}
        
        CONTENT BRIEFING:
        {briefing}
        
        TASK:
        Critique the briefing.
        1. Did it include all "Content Gaps"?
        2. Did it use the "Proof Keywords"?
        3. Is the structure logical?
        4. Are there any missing opportunities?

        OUTPUT:
        Provide a concise "Evaluation Report" with specific recommendations for improvement.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="text/plain"
                )
            )
            
            return response.text if response.text else "Error: Empty response from Gemini."

        except Exception as e:
            return f"Error evaluating briefing: {str(e)}"
