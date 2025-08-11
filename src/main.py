import streamlit as st
from components.layout import page_header, input_section, display_results
from components.pipeline import ask_cara_pipeline

st.set_page_config(page_title="Optimise with CARA", layout="wide")

def main():
    page_header()
    result = None  # initialize here to avoid undefined variable
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        content, run = input_section()
        if run and content.strip():
            with st.spinner("CARA is optimising..."):
                result = ask_cara_pipeline(content, "")  # no page_type param
            st.markdown("### Input Content")
            st.text_area("Your original content:", value=content, height=300, disabled=True)
        elif run:
            st.warning("Please provide content to process.")

    with col2:
        if result:
            display_results(result, original_text=None)
        else:
            st.info("Run optimisation to see governance report and suggestions here.")

if __name__ == "__main__":
    main()
