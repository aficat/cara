import streamlit as st

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Container: max width and center alignment */
        .main .block-container {
            max-width: 1100px;
            margin-left: auto;
            margin-right: auto;
            padding: 1.5rem 2rem;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(98, 71, 156, 0.15);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(128, 90, 213, 0.3);
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #2C2A4A;
        }

        /* Headers */
        h1, h2, h3, h4 {
            font-weight: 600;
            color: #5B3E96;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            letter-spacing: 0.02em;
        }

        /* Text readability */
        .main .block-container p, .main .block-container li, .stTextArea textarea {
            font-size: 1.125rem;
            line-height: 1.6;
            color: #3D3865;
        }

        /* Columns and layout spacing */
        [data-testid="stColumns"] > div {
            padding: 1rem;
            background: rgba(243, 240, 251, 0.8);
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(91, 62, 150, 0.1);
        }

        /* Buttons */
        .stButton > button {
            background-color: #FFFFFF !important;
            color: #6E46A1 !important;
            border: 2px solid #6E46A1 !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 0.6em 1.2em !important;
            transition: background-color 0.3s ease, color 0.3s ease !important;
        }
        .stButton > button:hover {
            background-color: #DCCEF8 !important;
            color: #111827 !important;
            border-color: #DCCEF8 !important;
        }
        .stButton > button:focus-visible {
            outline: 3px solid #111827 !important;
            outline-offset: 2px !important;
        }

        /* Link styles */
        a {
            color: #6B4C9A;
            text-decoration: none;
            font-weight: 500;
        }
        a:hover { text-decoration: underline; }
        a:focus-visible {
            outline: 3px solid #111827;
            outline-offset: 2px;
            border-radius: 4px;
        }

        /* Accessibility message emphasis */
        .stError { color: #D32F2F; font-weight: 700; }
        .stWarning { color: #F9A825; font-weight: 700; }
        </style>
        """,
        unsafe_allow_html=True,
    )
