import os
import json
from typing import Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path(__file__).resolve().parents[3] / '.env'
load_dotenv(dotenv_path=env_path)

class ContentBriefingClient:
    """
    A client for generating SEO Content Briefings using Gemini.
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
        # User requested Gemini 3 Pro Preview
        self.model = "gemini-2.5-pro" 

    def generate_briefing(self, report_data: Dict[str, Any], language: str = "German") -> str:
        """
        Generates a markdown content briefing based on the SEO report.

        Args:
            report_data: The full SEO report (keywords, competitors, semantics).
            language: The language for the briefing.

        Returns:
            Markdown string of the briefing.
        """
        
        # Serialize report data for the prompt
        report_json = json.dumps(report_data, indent=2, ensure_ascii=False)

        prompt = f"""
        You are an SEO Content Strategist. Create a detailed **Content Briefing** based on the provided SEO Report.
        
        SEO REPORT DATA:
        {report_json}
        
        TASK:
        Generate a structured Content Briefing in **{language}**.
        Follow this EXACT format and structure:

        CONTENT-BRIEFING: [Topic Name]
        
        1. FORMALE INFORMATIONEN
        Haupt-Keyword: [Main Keyword] ([Volume]/Monat)
        Neben-Keywords: [List of related keywords]
        Proof-Keywords: [List of semantic entities/proof keywords]
        Suchintention: Informational + Transaktional (Infer from data)
        Customer Journey: Consideration Phase (Infer from data)
        Textlänge: ca. 1.200-1.500 Wörter
        
        3. GLIEDERUNGSVORSCHLAG
        H1: [Compelling Title]
        H2: [Subheading]
         → [Brief content note]
        H2: [Subheading]
         H3: [Sub-subheading]
         H3: [Sub-subheading]
        H2: [Subheading addressing Content Gaps]
        H2: Unsere Top-Empfehlungen [+ Produktintegration]
        H2: Praktische Tipps: Anreise & beste Reisezeit
        
        6. SEO-HINWEISE
        Meta-Title: [Optimized Title with Main Keyword]
        Meta-Description: [Optimized Description with Call-to-Action]

        IMPORTANT:
        - Use the "Content Gaps" from the report to create specific H2/H3 sections.
        - Integrate "Entities" and "Proof Keywords" naturally into the outline notes.
        - Adopt a professional but inspiring tone.
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
            print(f"Error generating briefing: {e}")
            return f"Error generating briefing: {str(e)}"

if __name__ == "__main__":
    # Test with final_report.json if it exists, else dummy
    client = ContentBriefingClient()
    
    report_path = Path(__file__).resolve().parents[2] / "final_report.json"
    if report_path.exists():
        print(f"Loading report from {report_path}...")
        with open(report_path, "r") as f:
            report_data = json.load(f)
    else:
        print("Using dummy data...")
        report_data = {
            "topic": "Familienhotel Mallorca",
            "keyword_data": {"main_keyword": {"keyword": "familienhotel mallorca", "avg_searches": 8100}},
            "semantic_analysis": {
                "content_gaps": ["Budget options", "Teen activities"],
                "entities": {"concepts": ["All-Inclusive", "Pool"]}
            }
        }
    
    print("Generating Briefing...")
    briefing = client.generate_briefing(report_data, language="German")
    print("\n" + "="*40)
    print(briefing)
    print("="*40)
