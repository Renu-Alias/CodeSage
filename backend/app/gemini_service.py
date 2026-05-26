import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_with_gemini(code: str, language: str, mode: str = "Beginner") -> dict | None:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return None

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""You are CodeSage, a coding tutor for {mode} students.
Analyze the following {language} code and return ONLY valid JSON (no markdown, no backticks) with this exact structure:
{{
  "errors": [{{"line": <int>, "type": "<string>", "message": "<string>"}}],
  "suggestions": [{{"line": <int>, "title": "<string>", "message": "<string>"}}],
  "explanation": "<string with markdown>",
  "fixed_code": "<string>"
}}

Code:
{code}
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        import json
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        return json.loads(text.strip())

    except Exception as e:
        print(f"Gemini API error: {e}")
        return None
