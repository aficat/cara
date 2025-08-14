import streamlit as st
from components.layout import (
    page_header,
    input_section,
    display_content_score_card,
    display_content_columns_and_suggestions,
)
from components.pipeline import ask_cara_pipeline

st.set_page_config(page_title="Enable your content with CARAble", layout="wide")

# def login():
#     """Simple login form before showing main app."""
#     # If already logged in, don't show login again
#     if st.session_state.get("logged_in"):
#         return True

#     st.title("🔒 Login to use CARAble")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if username == st.secrets["auth"]["USER"] and password == st.secrets["auth"]["PASSWORD"]:
#             st.session_state["logged_in"] = True
#             st.rerun()  # Go to main app after login
#         else:
#             st.error("Invalid username or password")

#     return False


def main():
    page_header()

    # Input section with 2 columns: left input + right FAQ
    content, run = input_section()

    # Only show results after user clicks "Enable your content with CARAble"
    if run:
        if not content.strip():
            st.warning("Please provide content to process.")
            return
        
        st.divider()
        with st.spinner("CARAble is enabling your content..."):
            result = ask_cara_pipeline(content, "")

        # Content Score Card
        display_content_score_card(result)

        st.divider()

        # Input content on left, revised + suggestions on right
        display_content_columns_and_suggestions(result, content)
    else:
        st.divider()
        # FAQ handled in input_section already


if __name__ == "__main__":
    # if login():  # Only run main if logged in
        main()