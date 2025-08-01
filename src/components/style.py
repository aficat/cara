import streamlit as st

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Center content and constrain max width */
        .main .block-container {
            max-width: 900px;
            padding-left: 2rem;
            padding-right: 2rem;
            margin-left: auto;
            margin-right: auto;
            background-color: #fff;
            box-shadow: 0 2px 10px rgb(0 0 0 / 0.1);
            border-radius: 8px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Improve readability */
        .main .block-container p, .main .block-container li {
            font-size: 1.1rem;
            line-height: 1.6;
        }

        /* Optional: style headers */
        h1, h2, h3, h4 {
            font-weight: 600;
            margin-top: 1.2em;
            margin-bottom: 0.5em;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
