import streamlit as st
from components.layout import (
    page_header,
    input_section,
    display_content_score_card,
    display_content_columns_and_suggestions,
)
from components.pipeline import ask_cara_pipeline

st.set_page_config(page_title="Optimise with CARA", layout="wide")

# --- LOGIN FUNCTION ---
def login():
    st.title("🔒 Login to use CARA")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == st.secrets["USER"] and password == st.secrets["PASSWORD"]:
            st.session_state["logged_in"] = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

# --- MAIN APP FUNCTION ---
def main():
    page_header()

    # Input section with 2 columns: left input + right FAQ
    content, run = input_section()

    if run:
        if not content.strip():
            st.warning("Please provide content to process.")
            return
        
        st.divider()
        with st.spinner("CARA is optimising..."):
            result = ask_cara_pipeline(content, "")

        display_content_score_card(result)
        st.divider()
        display_content_columns_and_suggestions(result, content)
    else:
        st.divider()


# --- APP ENTRY POINT ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()
else:
    main()
