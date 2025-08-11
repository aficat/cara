import streamlit as st
from components.layout import page_header, input_section, display_results
from components.pipeline import ask_cara_pipeline

st.set_page_config(page_title="Optimise with CARA", layout="wide")

def main():
    page_header()
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        content, run = input_section()
    with col2:
        if run and content.strip():
            with st.spinner("CARA is optimising..."):
                result = ask_cara_pipeline(content, "")
                display_results(result, content)
        elif run:
            st.warning("Please provide content to process.")

if __name__ == "__main__":
    main()
