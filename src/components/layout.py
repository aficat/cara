import streamlit as st
from docx import Document
from bs4 import BeautifulSoup
import requests
import docx
from io import BytesIO
import streamlit.components.v1 as components

def page_header():
    with st.container():
        st.title("✨ CARAble")
        st.markdown(
            "<h3 style='margin-top: -10px; margin-bottom: 0.5rem; color: #5B3E96;'>Enable your content with CARA — your Content Authoring & Review Assistant</h3>",
            unsafe_allow_html=True,
        )
    st.divider()


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
            run = st.button("Enable your content with CARAble", use_container_width=True)

        with col2:
            faq_section()
            disclaimer_section()

    return content, run


def faq_section():
    st.markdown("### 💬 FAQs")
    with st.expander("Who is CARAble?"):
        st.markdown("""
CARAble is your helpful content assistant designed to support public officers in creating clear, citizen-friendly web pages — fast and confidently.

With CARAble, you can:
- Get smart recommendations for logical page structure and headings
- Rewrite content in a clear, professional tone suited for your audience
- Ensure your content meets WCAG accessibility standards
- Optimise your pages for SEO using trusted best practices
- Receive a detailed Governance Report Card  
- Easily compare your original and optimised content side-by-side
""")
    with st.expander("How do I get started and use CARAble?"):
        st.markdown("""
1. Submit your draft by pasting text, entering a gov.sg URL, or uploading a Word document.  
2. Click **Enable your content with CARAble** to start the review. 
3. View your content score card and detailed improvement suggestions.
4. Compare your original and optimised drafts to see the changes clearly.
5. Download your newly improved suggested copy.
""")
    with st.expander("Is CARAble still being improved?"):
        st.markdown("""
Yes, CARAble is a work in progress, and we’re committed to making it better over time to help you create clearer, more consistent, and compliant content.
""")
        
def disclaimer_section():
    st.markdown("### ❗Disclaimer")
    with st.expander("Important Notice"):
        st.markdown("""This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

Always consult with qualified professionals for accurate and personalised advice.
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
    return str(main_content)


def read_docx(uploaded_file) -> str:
    doc = Document(uploaded_file)
    full_text = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n".join(full_text)


def display_content_score_card(result: dict):
    st.markdown("### Content Score Card")

    scores = result.get("governance_report", {})
    structure_score = scores.get("structure_score", "N/A")
    tone_score = scores.get("tone_score", "N/A")
    accessibility_score = scores.get("accessibility_score", "N/A")
    seo_score = scores.get("seo_score", "N/A")

    cols = st.columns(4)
    cols[0].metric("Structure", f"{structure_score}")
    cols[1].metric("Tone", f"{tone_score}")
    cols[2].metric("Accessibility", f"{accessibility_score}")
    cols[3].metric("SEO", f"{seo_score}")

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
            components.html(original_wrapper, height=400, width=600, scrolling=True)
        with col2:
            st.markdown("### Improved Content")
            revised = result.get("revised_content", "")
            revised_wrapper = get_embedded_html_with_style(revised)
            components.html(revised_wrapper, height=400, width=600, scrolling=True)

            # Download as HTML
            st.download_button(
                label="Download as HTML",
                data=revised,
                file_name="revised_content.html",
                mime="text/html"
            )

            soup = BeautifulSoup(revised, "html.parser")
            doc = docx.Document()

            for elem in soup.recursiveChildGenerator():
                if elem.name:
                    if elem.name == "h1":
                        doc.add_heading(elem.get_text(), level=1)
                    elif elem.name == "h2":
                        doc.add_heading(elem.get_text(), level=2)
                    elif elem.name == "h3":
                        doc.add_heading(elem.get_text(), level=3)
                    elif elem.name == "p":
                        doc.add_paragraph(elem.get_text())
                    elif elem.name == "ul":
                        for li in elem.find_all("li"):
                            doc.add_paragraph(li.get_text(), style="List Bullet")
                    elif elem.name == "ol":
                        for li in elem.find_all("li"):
                            doc.add_paragraph(li.get_text(), style="List Number")

            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)

            st.download_button(
                label="Download as Word",
                data=buffer,
                file_name="revised_content.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
