import streamlit as st
from components.style import inject_custom_css
from components.layout import page_header, input_section, display_results
from components.pipeline import ask_cara_pipeline

st.set_page_config(page_title="Ask CARA - Content Authoring & Review Assistant", layout="wide")

def main():
    inject_custom_css()
    page_header()

    content_input, page_type, run_button = input_section()

    if run_button and content_input:
        with st.spinner("🧠 CARA is processing your inputs... this may take a few seconds"):
            try:
                result = ask_cara_pipeline(content_input, page_type)
                display_results(result)
            except Exception as e:
                st.error(f"⚠️ Something went wrong: {e}")
    else:
        st.caption("Paste content and hit the button above to start.")

main()
