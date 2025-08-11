# components/layout.py
import streamlit as st
from docx import Document
from bs4 import BeautifulSoup
import requests
import base64
import streamlit.components.v1 as components


def page_header():
    st.title("Optimise your content with CARA")

def input_section():
    st.markdown("### Submit your content")

    content = ""
    run_button = False

    input_type = st.radio(
        "Choose how to provide content:",
        ("URL (gov.sg only)", "Paste content", "Upload Word document"),
        index=0
    )

    if input_type == "URL (gov.sg only)":
        url = st.text_input("Enter a government website URL:", placeholder="https://www.gov.sg/...")
        if url and "gov.sg" not in url.lower():
            st.error("Only URLs from gov.sg are allowed.")
        elif url:
            try:
                content = fetch_webpage_text(url)
                if not content.strip():
                    st.error("No readable content found at the URL.")
                    content = ""
            except Exception as e:
                st.error(f"Failed to retrieve content: {e}")
                content = ""
        run_button = st.button("Optimise with CARA", use_container_width=True)

    elif input_type == "Paste content":
        content = st.text_area(
            "Paste your draft below:",
            height=250,
            placeholder="Paste your article or scheme draft here..."
        )
        run_button = st.button("Optimise with CARA", use_container_width=True)

    elif input_type == "Upload Word document":
        uploaded_file = st.file_uploader("Upload a .docx document", type=["docx"])
        if uploaded_file:
            try:
                content = read_docx(uploaded_file)
                if not content.strip():
                    st.error("The document appears to be empty.")
                    content = ""
            except Exception as e:
                st.error(f"Unable to read the document: {e}")
                content = ""
        run_button = st.button("Optimise with CARA", use_container_width=True)

    st.markdown("### CARA's Output")

    return content or "", input_type or "Unknown", run_button or False


def fetch_webpage_text(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # Prefer <main>, fallback to <body>
    main_content = soup.find("main")
    container = main_content if main_content else soup.find("body")

    if not container:
        return ""

    for tag in container(["script", "style", "nav", "footer", "header", "noscript", "form"]):
        tag.decompose()

    texts = container.stripped_strings
    return "\n".join(texts)


def read_docx(uploaded_file) -> str:
    doc = Document(uploaded_file)
    full_text = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n".join(full_text)


def highlight_differences(original: str, revised: str) -> str:
    import difflib

    differ = difflib.HtmlDiff(wrapcolumn=80)
    raw_html = differ.make_file(original.splitlines(), revised.splitlines(), context=True, numlines=3)

    custom_css = """
    <style>
        table.diff {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            border-collapse: collapse;
            width: 100%;
            margin-top: 1rem;
            font-size: 0.95rem;
        }
        table.diff th {
            background-color: #6a4c93;
            color: white;
            padding: 0.5em 1em;
            text-align: left;
            border-bottom: 2px solid #532e72;
        }
        table.diff td {
            padding: 0.5em 1em;
            vertical-align: top;
            white-space: pre-wrap;
            word-break: break-word;
        }
        table.diff tr {
            border-bottom: 1px solid #ddd;
        }
        .diff_add {
            background-color: #d4f7d4;
            color: #26532b;
        }
        .diff_chg {
            background-color: #f9d6d5;
            color: #7a2c2c;
        }
        .diff_sub {
            background-color: #fff;
            color: #444;
        }
        .diff_next {
            display: none;
        }
    </style>
    """

    if "<head>" in raw_html:
        parts = raw_html.split("<head>")
        head_and_rest = parts[1].split("</head>")
        new_html = parts[0] + "<head>" + custom_css + head_and_rest[0] + "</head>" + head_and_rest[1]
    else:
        new_html = custom_css + raw_html

    return new_html


def display_results(result: dict, original_text: str):
    st.markdown("## Summary")
    summary = result.get("summary") or result.get("governance_report", {}).get("summary") or "No summary available."
    st.info(summary)

    st.markdown("## Governance Report Card")
    scores = result.get("governance_report") or {}
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Structure", scores.get("structure_score", "N/A"))
    col2.metric("Tone of Voice", scores.get("tone_score", "N/A"))
    col3.metric("Accessibility", scores.get("accessibility_score", "N/A"))
    col4.metric("SEO", scores.get("seo_score", "N/A"))

    revised_text = result.get("revised_content") or result.get("rewritten_text", "")
    if original_text.strip() and revised_text.strip():
        st.markdown("## Original vs Rewritten Content")
        with st.expander("Compare content differences"):
            diff_html = highlight_differences(original_text, revised_text)
            components.html(diff_html, height=400, scrolling=True)
    else:
        st.warning("Both original and revised content are required for comparison.")

    if revised_text:
        b64 = base64.b64encode(revised_text.encode("utf-8")).decode()
        href = (
            f'<a href="data:text/plain;base64,{b64}" download="revised_content.txt">'
            f"📥 Download revised content as .txt</a>"
        )
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.info("No revised content available to download.")

    st.markdown("## Suggestions to Improve")

    structure = result.get("recommended_structure", [])
    if structure:
        st.markdown("### Structure")
        for s in structure:
            st.markdown(f"- {s}")

    tone = result.get("tone_fixes", [])
    if tone:
        st.markdown("### Tone of Voice")
        for t in tone:
            st.markdown(f"- {t}")

    accessibility = result.get("accessibility_fixes", [])
    if accessibility:
        st.markdown("### Accessibility")
        for a in accessibility:
            st.markdown(f"- {a}")

    seo = result.get("seo_fixes", [])
    if seo:
        st.markdown("### SEO")
        for s in seo:
            st.markdown(f"- {s}")

def page_faq():
    st.markdown("### Frequently Asked Questions")
    with st.expander("What is Optimise with CARA?"):
        st.markdown("""
        **Optimise with CARA** is your intelligent Content Authoring and Review Assistant — built to help public officers create clear, citizen-centric web pages.

        With CARA, you can:
        - Recommend logical structure and headers  
        - Rewrite in the appropriate tone and reading level  
        - Ensure content is WCAG-compliant and readable  
        - Optimise for SEO using global best practices  
        - Receive a Governance Report Card with areas to improve  
        - Compare original and optimised content side-by-side  
        """)