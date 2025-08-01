import json
import os
import re
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Load API key from Streamlit Secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Load API key from .env
# from dotenv import load_dotenv
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key, temperature=0.3)

def clean_response(raw_text: str) -> str:
    # Remove control characters except \n, \t (adjust if needed)
    cleaned = re.sub(r'[\x00-\x1f\x7f]', '', raw_text)
    return cleaned

def ask_cara_pipeline(raw_text: str, page_type: str) -> dict:
    prompt = f"""
You are CARA, the Content Authoring & Review Assistant. Your job is to help content authors structure, rewrite, and improve scheme/article pages.

INPUT:
- Page type: {page_type}
- Draft content: {raw_text}

TASKS:
1. Classify the content's intent.
2. Recommend a content compliant page structure (e.g., Who it’s for, How to apply).
3. Rewrite and restructure the draft using the right tone and content hierarchy (H1, H2, bullet points).
4. Perform WCAG 2.1 accessibility checks: fix unclear link text, missing alt text, heading hierarchy issues.
5. Perform SEO improvements: meaningful headings, internal link suggestions, keyword clarity.
6. Generate a Governance Report Card with: a summary of changes, structure compliance, tone alignment, accessibility and SEO improvements.

IMPORTANT: Please respond ONLY with valid JSON without any extra text or comments. Escape all special characters inside strings.

Respond in the following JSON format:
{{
  "intent": "...",
  "recommended_structure": ["...", "..."],
  "revised_content": "...",
  "accessibility_fixes": ["..."],
  "seo_fixes": ["..."],
  "governance_report": {{
    "structure_score": "...",
    "tone_score": "...",
    "accessibility_score": "...",
    "seo_score": "...",
    "summary": "..."
  }}
}}
"""
    response = llm([HumanMessage(content=prompt)])
    cleaned_response = clean_response(response.content)

    try:
        return json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON decode error: {e}\nRaw response:\n{cleaned_response}")
