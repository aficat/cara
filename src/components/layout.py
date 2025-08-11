import streamlit as st
from docx import Document
from bs4 import BeautifulSoup
import requests
import streamlit.components.v1 as components

def page_header():
    with st.container():
        st.title("Optimise with CARA")
        st.markdown(
            "<h3 style='margin-top: -10px; margin-bottom: 0.5rem; color: #5B3E96;'>Content Authoring & Review Assistant</h3>",
            unsafe_allow_html=True,
        )
    st.markdown("---")


def input_section():
    with st.container():
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.markdown("### Submit your content")
            input_type = st.radio(
                "Provide content via:",
                ("URL (gov.sg only)", "Paste content", "Upload Word document")
            )
            content = ""
            if input_type == "URL (gov.sg only)":
                url = st.text_input("Enter URL:")
                if url and "gov.sg" not in url.lower():
                    st.error("Only gov.sg URLs allowed.")
                elif url:
                    content = fetch_webpage_text(url) or ""
            elif input_type == "Paste content":
                content = st.text_area("Paste your draft:", height=250)
            elif input_type == "Upload Word document":
                uploaded_file = st.file_uploader("Upload .docx file", type=["docx"])
                if uploaded_file:
                    content = read_docx(uploaded_file)
            run = st.button("Optimise with CARA", use_container_width=True)

        with col2:
            faq_section()

    return content, run


def faq_section():
    st.markdown("### FAQs & About CARA")
    with st.expander("Who is CARA?"):
        st.markdown("""
CARA is your intelligent Content Authoring and Review Assistant — built to help public officers create clear, citizen-centric web pages.

With CARA, you can:
- Recommend logical structure and headers  
- Rewrite in the appropriate tone and reading level  
- Ensure content is WCAG-compliant and readable  
- Optimise for SEO using proven best practices  
- Receive a Governance Report Card  
- Compare original and optimised content side-by-side
""")
    with st.expander("How to use this app?"):
        st.markdown("""
1. Submit your content by pasting, URL, or uploading a Word document.  
2. Click **Optimise with CARA**.  
3. Review the content score card and suggested improvements.  
4. Compare your original and optimised content side-by-side.  
5. Download or copy the improved content for publishing.
""")
    with st.expander("Why is WCAG compliance important?"):
        st.markdown("""
Ensuring WCAG 2.1 compliance means your content is accessible to all users, including those with disabilities — improving usability and legal compliance.
""")


def fetch_webpage_text(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    main_content = soup.find("main") or soup.find("body")
    if not main_content:
        return ""
    for tag in main_content(["script", "style", "nav", "footer", "header", "noscript", "form"]):
        tag.decompose()
    texts = main_content.stripped_strings
    return "\n".join(texts)


def read_docx(uploaded_file) -> str:
    doc = Document(uploaded_file)
    full_text = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n".join(full_text)


def display_content_score_card(result: dict):
    st.markdown("### Content Score Card")
    cols = st.columns([1, 1, 1, 1], gap="small")
    scores = result.get("governance_report", {})
    labels = ["Structure", "Tone", "Accessibility", "SEO"]
    for col, label in zip(cols, labels):
        col.metric(label, scores.get(f"{label.lower()}_score", "N/A"))
    # Suggestions tabs below revised content
    st.markdown("### Suggestions")
    tabs = st.tabs(["Structure", "Tone", "Accessibility", "SEO"])

    suggestions_map = {
        "Structure": result.get("recommended_structure", []),
        "Tone": result.get("tone_fixes", []),
        "Accessibility": result.get("accessibility_fixes", []),
        "SEO": result.get("seo_fixes", [])
    }

    for tab, tab_label in zip(tabs, ["Structure", "Tone", "Accessibility", "SEO"]):
        with tab:
            items = suggestions_map.get(tab_label, [])
            if items:
                for item in items:
                    st.markdown(f"- {item}")
            else:
                st.write("No suggestions available.")


def display_content_columns_and_suggestions(result: dict, original_text: str):
    with st.container():
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            st.markdown("### Input Content")
            st.text_area("Original content:", value=original_text, height=400, disabled=True)
        with col2:
            st.markdown("### Improved Content")
            revised = result.get("revised_content", "")
            st.text_area("Optimised content:", value=revised, height=400, disabled=True)
