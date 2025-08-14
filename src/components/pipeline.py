import json
import os
import re
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import UnstructuredWordDocumentLoader
import nltk
from components.style import inject_custom_css


# Load API key from Streamlit Secrets
openai_api_key = st.secrets["api"]["OPENAI_API_KEY"]

# # Load API key from .env
# from dotenv import load_dotenv
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

inject_custom_css()

# -----------------------------
# Load Content Playbook
# -----------------------------
@st.cache_resource
def load_content_playbook():
    loader = UnstructuredWordDocumentLoader("src/resources/contentplaybook.docx")
    docs = loader.load()
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

# -----------------------------
# CARAble LLM initialization
# -----------------------------
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    openai_api_key=openai_api_key,
    temperature=0.1
)

MAX_CHARS = 5000  # LLM token limit approximation

# -----------------------------
# Utility functions
# -----------------------------
def clean_response(raw_text: str) -> str:
    """Remove control characters from raw model output (except \n, \t) and retain the heading types if any."""
    return re.sub(r'[\x00-\x1f\x7f]', '', raw_text)

def truncate_text(text: str, max_chars=MAX_CHARS) -> str:
    """Truncate text to max_chars while preserving line breaks, add truncation notice."""
    if len(text) <= max_chars:
        return text

    truncated = ""
    for line in text.splitlines(True):  # keep line breaks
        if len(truncated) + len(line) > max_chars:
            remaining = max_chars - len(truncated)
            truncated += line[:remaining]
            break
        truncated += line

    return truncated + "\n\n...[truncated]..."


# -----------------------------
# Guideline links for LLM reference
# -----------------------------
guideline_links = """
Accessibility references:
- WCAG 2.1 guidelines: https://www.w3.org/WAI/WCAG21/
- Lighthouse Accessibility Scoring: https://developer.chrome.com/docs/lighthouse/accessibility/scoring/

SEO references:
- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Lighthouse SEO audits: https://developer.chrome.com/docs/lighthouse/seo/link-text
- Meta description checks: https://developer.chrome.com/docs/lighthouse/seo/meta-description
- Font size guidelines: https://developer.chrome.com/docs/lighthouse/seo/font-size
"""

# -----------------------------
# Core CARAble pipeline
# -----------------------------
def ask_cara_pipeline(raw_text: str, page_type: str) -> dict:
    """Core CARAble pipeline to process content using tone, structure, accessibility, and SEO logic.
    Process content using CARAble:
    - Preserve headings, paragraphs, bullets, tables
    - Apply content playbook, WCAG, and SEO checks
    - Output JSON with revised content and report card
    """

    truncated_text = truncate_text(raw_text)
    vectorstore = load_content_playbook()

    # Retrieve relevant guidelines from content playbook
    related_guidelines = vectorstore.similarity_search(truncated_text, k=5)
    guidelines_text = "\n".join([doc.page_content for doc in related_guidelines])

    prompt = f"""
You are CARAble, the Content Authoring & Review Assistant.

References from CONTENT PLAYBOOK:
{guidelines_text}

References from GUIDELINES LINKS:
{guideline_links}

INPUT:
- Page type: {page_type}
- Draft content: {truncated_text}

OBJECTIVES:
- Produce citizen-facing content that is accessible, well-structured, and search-optimized.
- Provide paraphrasing based on tone, structure, voice, accessibility, and SEO, while retaining original meaning and content.
- Inputs and outputs should remain in textual HTML formats with headings, paragraphs, hyperlinks, tables, bullets, links, or numbered points.
- Do not omit any content from the original draft. The output content should not be a summary or condensed version.
- The word count before and after should be similar, with no significant reduction in content length.
- Retain original content length (do not omit content)
- Preserve all headings (H2/H3), paragraphs, lists, and tables
- Apply tone, structure, accessibility (WCAG 2.1), and SEO improvements
- Check against the CONTENT PLAYBOOK and GUIDELINES LINKS as well


TASKS:
1. Recommend an ideal content structure with headings e.g. H3: <content>. Typically, article and scheme pages starts their title with H2 and the subheaders are H3. 
2. Rephrase the draft with:
   - Clear, helpful, professional tone aligned to the Content Playbook word document
   - Consistent voice aligned to the Content Playbook word document
   - Check against all sections and topics within the Content Playbook word document
   - Logical heading levels, bullet points or numbered lists
   - Improved readability, scannability, and service clarity
   - Ensure none of the draft is omitted
3. Apply **WCAG 2.1 accessibility** checks:
   - Heading hierarchy
   - Descriptive link text
   - Alt text recommendations
   - Simplify complex language
   - Contrast, navigation, and keyboard accessibility
   - Accessibility lighthouse checks
   - WCAG 2.1 AA compliance from the official WCAG 2.1 guidelines
4. Apply **SEO best practices**:
   - Keyword-rich headings
   - Meta description clarity
   - Internal linking suggestions
   - Font size legibility
   - Mobile-first readability
   - Google SEO Starter Guide checks
   - Google Lighthouse SEO checks
5. Generate a **Governance Report Card**:
   - Structure, tone, accessibility, and SEO scores
   - Summary of fixes and rewrites with specific examples of where it should be changed and what it should be changed to
   - Before/after comparison of major improvements

OUTPUT FORMAT:
- Content score card values out of 10, format: score/10.
- Remove elements: "script", "nav", "footer", "header", "noscript", "form", "img", "button", "input", "select"
- Return only valid **JSON** with string or string-array values. No extra text or commentary.

Format:
{{
  "recommended_structure": ["...", "..."],
  "revised_content": "...",
  "accessibility_fixes": ["..."],
  "seo_fixes": ["..."],
  "tone_fixes": ["..."],
  "governance_report": {{
    "structure_score": "...",
    "tone_score": "...",
    "accessibility_score": "...",
    "seo_score": "...",
    "summary": "..."
  }}
}}"""
    
    response = llm([
        SystemMessage(content="You are CARAble, a Content Authoring & Review Assistant."),
        HumanMessage(content=prompt)
    ])
    
    cleaned = clean_response(response.content)
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON decode error: {e}\nRaw response:\n{cleaned}")