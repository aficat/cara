# main.py
import streamlit as st
from components.style import inject_custom_css
from components.layout import page_header, input_section, display_results, page_faq
from components.pipeline import ask_cara_pipeline

st.set_page_config(page_title="Optimise your web content with CARA", layout="wide")

def main():
    inject_custom_css()
    page_header()

    content, input_type, run_button = input_section()

    if run_button and content:
        with st.spinner("🧠 CARA is processing your inputs... this may take a few seconds"):
            try:
                result = ask_cara_pipeline(content, input_type)
                display_results(result, original_text=content)
            except Exception as e:
                # Keep it concise but useful
                st.error(f"⚠️ Something went wrong while optimising your content: {e}")
    else:
        st.caption("Provide content via URL, paste, or Word doc upload, then click ‘Optimise with CARA’.")

    page_faq()

if __name__ == "__main__":
    main()
