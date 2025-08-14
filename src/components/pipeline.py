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

# Load API key from Streamlit Secrets
openai_api_key = st.secrets["api"]["OPENAI_API_KEY"]

# Load API key from .env
# from dotenv import load_dotenv
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

# Cache loading of content playbook
def load_content_playbook():
    loader = UnstructuredWordDocumentLoader("src/resources/contentplaybook.docx")
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

def ask_cara_pipeline(raw_text: str, page_type: str) -> dict:
    """Core CARAble pipeline to process content using tone, structure, accessibility, and SEO logic."""

    truncated_text = truncate_text(raw_text)
    vectorstore = load_content_playbook()

    # Retrieve relevant guidelines from content playbook
    related_guidelines = vectorstore.similarity_search(truncated_text, k=5)
    guidelines_text = "\n".join([doc.page_content for doc in related_guidelines])

    guidelines = """
    Accessibility:
    - Follow WCAG 2.1 guidelines for headings, contrast, navigation, link text, and readability.
    - Incorporate Lighthouse Accessibility best practices (keyboard navigation, alt text, clear structure).

    SEO:
    - Follow Google SEO Starter Guide: meaningful headings, meta descriptions, keyword placement.
    - Lighthouse SEO checks: descriptive link text, mobile readability, font legibility, meta description checks.
    """

    prompt = f"""
You are CARAble, the Content Authoring & Review Assistant. Use the following **Content Playbook guidelines** to review and rewrite content:

Content Playbook Guidelines:
{guidelines_text}

INPUT:
- Page type: {page_type}
- Draft content: {truncated_text}

REFERENCES:
- {guidelines_text} Content Playbook rules from the Content Playbook word document
- {guidelines}

OBJECTIVES:
- Produce citizen-facing content that is accessible, well-structured, and search-optimized.
- Provide paraphrasing based on tone, structure, voice, accessibility, and SEO, while retaining original meaning and content.
- Inputs and outputs should remain in textual HTML formats with headings, paragraphs, hyperlinks, tables, bullets, links, or numbered points.
- Do not omit any content from the original draft. The output content should not be a summary or condensed version.
- The word count before and after should be similar, with no significant reduction in content length.

TASKS:
1. Identify the **intent** and **purpose** of the content.
2. Recommend an ideal content structure with headings e.g. H3: <content>. Typically, article and scheme pages starts their title with H2 and the subheaders are H3. 
3. Rephrase the draft with:
   - Clear, helpful, professional tone aligned to the Content Playbook word document
   - Consistent voice aligned to the Content Playbook word document
   - Check against all sections and topics within the Content Playbook word document
   - Logical heading levels, bullet points or numbered lists
   - Improved readability, scannability, and service clarity
   - Ensure none of the draft is omitted
4. Apply **WCAG 2.1 accessibility** checks:
   - Heading hierarchy
   - Descriptive link text
   - Alt text recommendations
   - Simplify complex language
   - Contrast, navigation, and keyboard accessibility
   - Accessibility lighthouse checks
   - WCAG 2.1 AA compliance from the official WCAG 2.1 guidelines
5. Apply **SEO best practices**:
   - Keyword-rich headings
   - Meta description clarity
   - Internal linking suggestions
   - Font size legibility
   - Mobile-first readability
   - Google SEO Starter Guide checks
   - Google Lighthouse SEO checks
6. Generate a **Governance Report Card**:
   - Structure, tone, accessibility, and SEO scores
   - Summary of fixes and rewrites with sepecific examples of where it should be changed and what it should be changed to
   - Before/after comparison of major improvements

OUTPUT FORMAT:
- Return only valid **JSON** with string or string-array values. No extra text or commentary.
- Content score card values out of 10, format: score/10.
- Remove elements: "script", "nav", "footer", "header", "noscript", "form", "img", "button", "input", "select"

Format:
{{
  "intent": "...",
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
}}
"""

    response = llm([
        SystemMessage(content="You are CARAble, a Content Authoring & Review Assistant that overlooks content quality and governance."),
        HumanMessage(content=prompt)
    ])

    cleaned_response = clean_response(response.content)

    try:
        return json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON decode error: {e}\nRaw response:\n{cleaned_response}")