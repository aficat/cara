import streamlit as st
from docx import Document
from bs4 import BeautifulSoup
import requests

def page_header():
    st.title("Ask CARA 🧠")
    st.subheader("Your personal Content Authoring & Review Assistant (CARA)")
    st.markdown("""
    Ask CARA helps product owners and content authors confidently create high-quality citizen-facing scheme and article pages.
    Paste your draft, upload a file, or enter a CPF webpage URL, and CARA will:
    - Recommend structure and headers
    - Rewrite content in the right voice and hierarchy
    - Check for accessibility and SEO compliance
    - Generate a before/after governance report
    """)

def input_section():
    st.markdown("### Select input type:")
    input_type = st.radio(
        "Choose how you want to provide content:",
        ("Hyperlink (cpf.gov.sg only)", "Paste Content", "Upload Word Document")
    )

    content = ""
    run_button = False

    with st.container():
        if input_type == "Hyperlink (cpf.gov.sg only)":
            url = st.text_input("Enter CPF.gov.sg URL:", placeholder="https://www.cpf.gov.sg/...")
            col1, col2 = st.columns([3,1])
            with col2:
                run_button = st.button("✨ Optimise with Ask CARA", use_container_width=True)
            if url and "cpf.gov.sg" not in url.lower():
                st.error("⚠️ Please enter a valid URL from cpf.gov.sg only.")
            elif url:
                try:
                    content = fetch_webpage_text(url)
                    if not content.strip():
                        st.error("⚠️ Could not extract content from the webpage.")
                        content = ""
                except Exception as e:
                    st.error(f"⚠️ Failed to fetch or parse the webpage: {e}")
                    content = ""

        elif input_type == "Paste Content":
            content = st.text_area(
                "✍️ Paste your draft scheme/article page here:",
                height=300,
                placeholder="Paste your CPF scheme or article content here..."
            )
            run_button = st.button("✨ Optimise with Ask CARA", use_container_width=True)

        elif input_type == "Upload Word Document":
            uploaded_file = st.file_uploader(
                "Upload a Word document (.docx)",
                type=["docx"],
                help="Upload a .docx file containing your draft content."
            )
            run_button = st.button("✨ Optimise with Ask CARA", use_container_width=True)
            if uploaded_file:
                try:
                    content = read_docx(uploaded_file)
                    if not content.strip():
                        st.error("⚠️ Uploaded document is empty.")
                except Exception as e:
                    st.error(f"⚠️ Could not read Word document: {e}")
                    content = ""

    return content, "Unknown", run_button

def fetch_webpage_text(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "form"]):
        tag.decompose()

    texts = soup.stripped_strings
    return "\n".join(texts)

def read_docx(uploaded_file) -> str:
    doc = Document(uploaded_file)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)

def display_results(result: dict):
    st.markdown("### 🧭 Page Intent")
    st.code(result.get('intent', 'N/A'), language='markdown')

    st.markdown("### 🧱 Recommended Structure")
    st.markdown("\n".join(f"- {h}" for h in result.get('recommended_structure', [])))

    st.markdown("### ✍️ Revised Content")
    st.text_area("Optimised Content:", result.get('revised_content', ''), height=300)

    st.markdown("### ♿ Accessibility Fixes")
    for fix in result.get('accessibility_fixes', []):
        st.markdown(f"- {fix}")

    st.markdown("### 🔍 SEO Fixes")
    for fix in result.get('seo_fixes', []):
        st.markdown(f"- {fix}")

    st.markdown("### 📊 Governance Report Card")
    scores = result.get('governance_report', {})
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Structure Score", scores.get('structure_score', 'N/A'))
    metric_col2.metric("Tone Score", scores.get('tone_score', 'N/A'))
    metric_col3.metric("Accessibility Score", scores.get('accessibility_score', 'N/A'))
    metric_col4.metric("SEO Score", scores.get('seo_score', 'N/A'))

    st.markdown("#### Summary")
    st.info(scores.get('summary', ''))
