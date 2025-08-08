import json
import os
import re
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.schema import SystemMessage

# Load API key from Streamlit Secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Load API key from .env
# from dotenv import load_dotenv
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model_name="gpt-4",
    openai_api_key=openai_api_key,
    temperature=0.3
)

def clean_response(raw_text: str) -> str:
    """Remove control characters from raw model output (except \n, \t)."""
    return re.sub(r'[\x00-\x1f\x7f]', '', raw_text)

def ask_cara_pipeline(raw_text: str, page_type: str) -> dict:
    """Core CARA pipeline to process content using tone, SEO, and WCAG logic."""

    prompt = f"""
You are CARA, the Content Authoring & Review Assistant developed for public content. Your job is to help authors rewrite and improve pages to meet content governance playbook and global accessibility (WCAG 2.1) and SEO standards.

INPUT:
- Page type: {page_type}
- Draft content: {raw_text}

OBJECTIVES:
- Produce citizen-facing content that is accessible, well-structured, and search-optimised
- Provide rewrites based on content tone, structure, and information hierarchy

TASKS:
1. Identify the **intent** and **purpose** of the content
2. Recommend an ideal content structure (e.g., "Who it’s for", "How to qualify", "How to apply")
3. Rewrite the draft with:
   - Clear, helpful, professional tone of voice
   - Logical heading levels (H1, H2, bullet points)
   - Improved readability, scannability, and service clarity

4. Apply **WCAG 2.1 accessibility** checks:
   - Improve heading hierarchy and reading order
   - Flag or fix unclear or generic link text (e.g. "click here")
   - Recommend descriptive alt text for any referenced images
   - Simplify complex language
   - Ensure good contrast, consistent navigation, and keyboard-friendly formatting (if relevant)

5. Apply **SEO best practices**:
   - Use meaningful, keyword-rich headings
   - Highlight key terms near the top
   - Suggest internal linking to relevant pages (if applicable)
   - Remove redundant phrasing and improve meta clarity
   - Prioritise mobile-first readability (short paragraphs, clear CTA)

6. Generate a **Governance Report Card**:
   - Structure, tone, accessibility, and SEO scores
   - Summary of fixes and rewrites
   - Before/after comparison of major improvements

OUTPUT FORMAT:
Return only valid **JSON** (no extra text, no comments). All values must be strings or string arrays. Escape special characters properly.

Format:
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

    response = llm([
        SystemMessage(content="You are CARA, a content governance assistant."),
        HumanMessage(content=prompt)
    ])

    cleaned_response = clean_response(response.content)

    try:
        return json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON decode error: {e}\nRaw response:\n{cleaned_response}")
