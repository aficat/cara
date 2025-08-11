import streamlit as st
from docx import Document
from bs4 import BeautifulSoup
import requests
import base64
import streamlit.components.v1 as components


def page_header():
    st.title("Optimise with CARA")
    st.subheader("Content Authoring & Review Assistant")
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


def input_section():
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
    return content, run


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


def display_results(result: dict, original_text: str = None):
    # Show governance report card on top
    st.markdown("### Governance Report Card")
    cols = st.columns([1, 1, 1, 1], gap="small")
    scores = result.get("governance_report", {})
    labels = ["Structure", "Tone", "Accessibility", "SEO"]
    for col, label in zip(cols, labels):
        col.metric(label, scores.get(f"{label.lower()}_score", "N/A"))

    # Show output text area for revised content
    revised = result.get("revised_content", "")
    if revised:
        st.markdown("### Revised Content")
        st.text_area("Optimised content:", value=revised, height=300, disabled=True)

    # Suggestions tab for improvements in structure, tone, accessibility, SEO
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
