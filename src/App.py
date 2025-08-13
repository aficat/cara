import streamlit as st
from components.layout import (
    page_header,
    input_section,
    display_content_score_card,
    display_content_columns_and_suggestions,
)
from components.pipeline import ask_cara_pipeline

st.set_page_config(page_title="Optimise with CARA", layout="wide")

def main():
    page_header()

    # Input section with 2 columns: left input + right FAQ
    content, run = input_section()

    # Only show results after user clicks "Optimise with CARA"
    if run:
        if not content.strip():
            st.warning("Please provide content to process.")
            return
        
        st.divider()
        with st.spinner("CARA is optimising..."):
            result = ask_cara_pipeline(content, "")

        # Content Score Card container (replaces Governance Report Card heading)
        display_content_score_card(result)

        st.divider()

        # Show input content on left, revised content + suggestions on right
        display_content_columns_and_suggestions(result, content)
    else:
        st.divider()
        # Show FAQ on right column of input_section (already rendered there)
        # No extra output below until user clicks run


if __name__ == "__main__":
    main()
