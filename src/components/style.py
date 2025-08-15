import streamlit as st

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Container */
        .main .block-container {
            max-width: 1100px;
            margin-left: auto;
            margin-right: auto;
            padding: 1.5rem 2rem;
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(107, 63, 207, 0.15); /* soft purple shadow */
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(107, 63, 207, 0.3);
            font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
                 Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            color: #4B0082; /* dark indigo text */
        }

        /* Headers */
        h1, h2, h3, h4 {
            font-weight: 600;
            color: #6A0DAD; /* vibrant purple */
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            letter-spacing: 0.02em;
        }

        /* Text readability */
        .main .block-container p, 
        .main .block-container li, 
        .stTextArea textarea {
            font-size: 1.125rem;
            line-height: 1.6;
            color: #4B0082; /* dark purple for readability */
        }

        /* Columns and layout spacing */
        [data-testid="stColumns"] > div {
            padding: 1rem;
            background: rgba(230, 215, 255, 0.85); /* light purple */
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(107, 63, 207, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        [data-testid="stColumns"] > div:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(107, 63, 207, 0.12);
        }

        /* Buttons */
        .stButton > button {
            background-color: #E0D0FF !important; /* light purple background */
            color: #4B0082 !important;            
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 0.6em 1.2em !important;
            transition: background-color 0.3s ease, color 0.3s ease !important;
        }
        .stButton > button:hover {
            background-color: #D0B3FF !important;
            color: white !important;
        }
        .stButton > button:focus-visible {
            outline: 3px solid #6A0DAD !important;
            outline-offset: 2px !important;
        }
        .st-emotion-cache-5qfegl {
            background-color: #E0D0FF !important; /* light purple background */
            color: #4B0082 !important;            
            border: 2px solid #6A0DAD !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 0.6em 1.2em !important;
            transition: background-color 0.3s ease, color 0.3s ease !important;
        }
        .st-emotion-cache-5qfegl:hover {
            background-color: #D0B3FF !important;
            color: white !important;
            border-color: #6A0DAD !important;
        }
        .st-emotion-cache-5qfegl:focus-visible {
            outline: 3px solid #6A0DAD !important;
            outline-offset: 2px !important;
        }

        /* Radio buttons & checkboxes */
        div[data-baseweb="radio"] label, 
        div[data-baseweb="checkbox"] label {
            color: #6A0DAD !important; 
            font-weight: 500;
        }
        div[data-baseweb="radio"] input:checked + label::before, 
        div[data-baseweb="checkbox"] input:checked + label::before {
            background-color: #6A0DAD !important; /* purple fill */
            border-color: #6A0DAD !important;
        }
        .st-av {
            background-color: #6A0DAD !important; 
        }
        .st-cr{
            background-color: #6A0DAD !important; 
        }
        
        /* Hyperlinks */
        a {
            color: #6A0DAD;
            text-decoration: none;
            font-weight: 500;
        }
        a:hover { text-decoration: underline; }
        a:focus-visible {
            outline: 3px solid #6A0DAD;
            outline-offset: 2px;
            border-radius: 4px;
        }
        .st-emotion-cache-r44huj a {
            color: #6A0DAD;
            text-decoration: none;
            font-weight: 500;
        }
        .st-emotion-cache-r44huj a:hover { text-decoration: underline; }
        .st-emotion-cache-r44huj a:focus-visible {
            outline: 3px solid #6A0DAD;
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
