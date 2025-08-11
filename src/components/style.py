# components/style.py
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

        /* Scrollable diffs container */
        iframe, .streamlit-expanderHeader {
            font-family: 'Inter', sans-serif;
        }

        /* Buttons */
        .stButton > button {
            background-color: #FFFFFF !important;     /* White fill */
            color: #6E46A1 !important;                /* Purple text */
            border: 2px solid #6E46A1 !important;     /* Purple outline */
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 0.6em 1.2em !important;
            transition: background-color 0.3s ease, color 0.3s ease !important;
        }
        .stButton > button:hover {
            background-color: #DCCEF8 !important;     /* Lighter purple fill on hover */
            color: #111827 !important;                /* Dark text on hover */
            border-color: #DCCEF8 !important;
        }
        .stButton > button:focus-visible {
            outline: 3px solid #111827 !important;    /* High-contrast focus ring */
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
        .stError { color: #D32F2F; font-weight: 600; }
        .stWarning { color: #B45309; font-weight: 600; }

        /* TextArea resize control */
        textarea {
            resize: vertical;
            min-height: 150px;
            max-height: 400px;
        }

        /* Respect reduced motion preferences */
        @media (prefers-reduced-motion: reduce) {
            * { transition: none !important; animation: none !important; }
        }

        /* Responsive tweaks */
        @media (max-width: 768px) {
            .main .block-container { padding: 1rem 1.5rem; }
            [data-testid="stColumns"] > div { padding: 0.5rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
