import json
import os
import re
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# For PDF loading and vector search
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load API key from Streamlit Secrets
openai_api_key = st.secrets["api"]["OPENAI_API_KEY"]

# Load API key from .env
# from dotenv import load_dotenv
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

# Cache loading of content playbook
@st.cache_resource(show_spinner=False)
def load_content_playbook():
    loader = PyPDFLoader("src/resources/contentplaybook.pdf") 
    docs = loader.load()
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

# Initialize LLM and playbook retriever once
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    openai_api_key=openai_api_key,
    temperature=0.1
)

MAX_CHARS = 8000  # Rough limit to keep token count under max context length

def clean_response(raw_text: str) -> str:
    """Remove control characters from raw model output (except \n, \t)."""
    return re.sub(r'[\x00-\x1f\x7f]', '', raw_text)

def truncate_text(text: str, max_chars=MAX_CHARS) -> str:
    """Truncate text to max_chars, add truncation notice."""
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n...[truncated]..."
    return text

def ask_cara_pipeline(raw_text: str, page_type: str) -> dict:
    """Core CARA pipeline to process content using tone, SEO, and WCAG logic."""

    truncated_text = truncate_text(raw_text)

    prompt = f"""
You are CARA, the Content Authoring & Review Assistant developed for public content. Your job is to help authors rewrite and improve pages to meet content governance playbook and global accessibility (WCAG 2.1) and SEO standards.

INPUT:
- Page type: {page_type}
- Draft content: {truncated_text}

OBJECTIVES:
- Produce citizen-facing content that is accessible, well-structured, and search-optimised
- Provide paraphrasing based on content tone, structure, and information hierarchy
- Inputs and outputs should be in textual HTML formats in headings, paragraphs, tables, bulleted, hyperlinks or numbered points.

TASKS:
1. Identify the **intent** and **purpose** of the content
2. Recommend an ideal content structure
3. Rephrase the draft with:
   - Clear, helpful, professional tone of voice
   - Logical heading levels (H1, H2, bullet points)
   - Improved readability, scannability, and service clarity
   - Ensure none of the draft is omitted
   - Retain the paragraph structure of the original draft

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
- Return only valid **JSON** (no extra text, no comments). 
- All values must be strings or string arrays. 
- Escape special characters properly.
- Content score card results will always be scored out of 10 points and display in the format of score/10.
- Ensure none of the content is omitted.
- Remove elements such as "script", "nav", "footer", "header", "noscript", "form", "img", "button", "input", "select"

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