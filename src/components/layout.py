import streamlit as st
from docx import Document
from bs4 import BeautifulSoup
import requests
import docx
from io import BytesIO
import streamlit.components.v1 as components

def page_header():
    with st.container():
        st.title("✨ Optimise with CARA")
        st.markdown(
            "<h3 style='margin-top: -10px; margin-bottom: 0.5rem; color: #5B3E96;'>Your personal Content Authoring & Review Assistant</h3>",
            unsafe_allow_html=True,
        )
    st.markdown("---")


def input_section():
    with st.container():
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.markdown("### 📝 Start your content review")
            input_type = st.radio(
                "Choose how you'd like to provide your draft",
                ("Website URL", "Paste your draft directly", "Upload a Word document")
            )
            content = ""
            if input_type == "Website URL":
                url = st.text_input("Enter URL (gov.sg sites only)")
                if url and "gov.sg" not in url.lower():
                    st.error("Only gov.sg URLs allowed.")
                elif url:
                    content = fetch_webpage_text(url) or ""
            elif input_type == "Paste your draft directly":
                content = st.text_area("Paste your draft", height=250)
            elif input_type == "Upload a Word document":
                uploaded_file = st.file_uploader("Upload .docx file", type=["docx"])
                if uploaded_file:
                    content = read_docx(uploaded_file)
            run = st.button("Optimise with CARA", use_container_width=True)

        with col2:
            faq_section()

    return content, run


def faq_section():
    st.markdown("### 💬 FAQs about CARA")
    with st.expander("Who is CARA?"):
        st.markdown("""
CARA is your helpful content assistant designed to support public officers in creating clear, citizen-friendly web pages — fast and confidently.

With CARA, you can:
- Get smart recommendations for logical page structure and headings
- Rewrite content in a clear, professional tone suited for your audience
- Ensure your content meets WCAG accessibility standards
- Optimise your pages for SEO using trusted best practices
- Receive a detailed Governance Report Card  
- Easily compare your original and optimised content side-by-side
""")
    with st.expander("How do I get started and use CARA?"):
        st.markdown("""
1. Submit your draft by pasting text, entering a gov.sg URL, or uploading a Word document.  
2. Click **Optimise with CARA** to start the review. 
3. View your content score card and detailed improvement suggestions.
4. Compare your original and optimised drafts to see the changes clearly.
5. Download or copy your newly improved suggested copy.
""")
    with st.expander("Why is content governance important?"):
        st.markdown("""
Content governance helps you create clear, consistent, and compliant web pages—fast. It saves you time, ensures a unified tone and brand, makes content accessible to everyone, and reduces risk by meeting standards.

In short, it lets you work smarter while delivering trustworthy, user-friendly content.
""")
    with st.expander("Is CARA still being improved?"):
        st.markdown("""
Yes, CARA is a work in progress, and we’re committed to making it better over time to help you create clearer, more consistent, and compliant content.
""")


def fetch_webpage_text(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    main_content = soup.find("main") or soup.find("body")
    if not main_content:
        return ""

    # Remove unwanted tags
    for tag in main_content(["script", "nav", "footer", "header", "noscript", "form", "img", "button", "input", "select"]):
        tag.decompose()

    # Remove social media bars (common class/id keywords)
    social_selectors = [
        '[class*="social"]',
        '[class*="share"]',
        '[class*="follow"]',
        '[class*="fb"]',
        '[class*="twitter"]',
        '[class*="instagram"]',
        '[class*="linkedin"]',
        '[class*="pinterest"]',
        '[id*="social"]',
        '[id*="share"]',
        '[id*="follow"]',
    ]

    for selector in social_selectors:
        for elem in main_content.select(selector):
            elem.decompose()

    # Return inner HTML instead of plain text
    return str(main_content)

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

def get_embedded_html_with_style(html_content: str) -> str:
    embedded_css = """
    <style>
    body {
        font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
            Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        color: #3D3865;
        padding: 1rem;
    }
    h1, h2, h3 {
        color: #5B3E96;
        font-weight: 600;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    p {
        font-size: 1.1rem;
        line-height: 1.5;
        margin-bottom: 1em;
    }
    a {
        color: #6B4C9A;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1rem;
    }
    th, td {
        border: 1px solid #ccc;
        padding: 0.5rem;
        text-align: left;
    }
    </style>
    """
    return f"""
    {embedded_css}
    <div>
        {html_content}
    </div>
    """

def display_content_columns_and_suggestions(result: dict, original_text: str):
    with st.container():
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            st.markdown("### Input Content")
            original_wrapper = get_embedded_html_with_style(original_text)
            components.html(original_wrapper, height=400, scrolling=True)
            # with st.expander("View code"):
            #     st.code(original_text, language="html", height=400)
        with col2:
            # st.badge("Newly revised", color="violet")
            st.markdown("### Improved Content")
            revised = result.get("revised_content", "")
            revised_wrapper = get_embedded_html_with_style(revised)
            # revised_html_with_wrapper = f'<div class="embedded-html">{revised}</div>'
            components.html(revised_wrapper, height=400, scrolling=True)
            # with st.expander("View code"):
            #     st.code(revised, language="html", height=400)
            
            # Download as HTML
            st.download_button(
                label="Download as HTML",
                data=revised,
                file_name="revised_content.html",
                mime="text/html"
            )

            # Download as Word docx
            soup = BeautifulSoup(revised, "html.parser")
            plain_text = soup.get_text()

            doc = docx.Document()
            doc.add_paragraph(plain_text)
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)

            st.download_button(
                label="Download as Word",
                data=buffer,
                file_name="revised_content.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
