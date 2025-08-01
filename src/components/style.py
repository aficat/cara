import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
        body {
            background-color: #f4f6f9;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .stTextArea textarea {
            font-size: 16px !important;
            line-height: 1.5 !important;
        }
        .stButton button {
            background-color: #0064b5 !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 0.5em 1.2em !important;
            font-weight: 600 !important;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #004e91 !important;
        }
        .report-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1em;
            background-color: #fff;
            margin-bottom: 1em;
        }
        .metric-container {
            display: flex;
            justify-content: space-around;
            gap: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
