import os
import threading
import time
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_TIMEOUT = 2

def analyze_with_gemini(code: str, language: str, mode: str = "Beginner") -> dict | None:
    if not GEMINI_API_KEY or GEMINI_API_KEY in ["your_gemini_api_key_here", "YOUR_API_KEY_HERE", "YOUR_API_KEY"]:
        return None

    result = []
    exception = []

    def _call():
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_API_KEY)

            explanation_style = (
                "Explain in super simple language like you're talking to a total beginner. "
                "Use everyday analogies (like recipes, toys, or games). "
                "Break down each line with simple examples. "
                "No jargon. If you must use a technical word, explain it right after."
            ) if mode.lower() == "beginner" else (
                "Explain in technical terms suitable for an intermediate programmer. "
                "Discuss edge cases, performance, and best practices."
            )

            prompt = f"""You are CodeSage, a friendly coding tutor for {mode} students.

{explanation_style}

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
            result.append(json.loads(text.strip()))
        except Exception as e:
            exception.append(e)

    thread = threading.Thread(target=_call, daemon=True)
    thread.start()
    thread.join(timeout=GEMINI_TIMEOUT)

    if thread.is_alive():
        print("Gemini API timed out — falling back to local analyzer")
        return None

    if exception:
        print(f"Gemini API error: {exception[0]}")
        return None

    return result[0] if result else None
