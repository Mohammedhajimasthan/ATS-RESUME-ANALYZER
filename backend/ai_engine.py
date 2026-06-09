import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def analyze_resume(resume_text: str, job_desc: str):
    if not client:
        return {
            "score": 0,
            "strengths": ["AI key not configured"],
            "weaknesses": [],
            "improvements": [],
            "questions": []
        }

    prompt = f"""
You are an ATS Resume Evaluator.

Resume:
{resume_text}

{f"Job Description: {job_desc}" if job_desc else ""}

Return ONLY valid JSON in this format:
{{
  "score": number (0-100),
  "strengths": [string],
  "weaknesses": [string],
  "improvements": [string],
  "questions": [string]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
