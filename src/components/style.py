import streamlit as st

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* CSS Custom Properties for consistent theming */
        :root {
            --primary-color: #7c3aed; /* Violet 600 - modern violet */
            --primary-hover: #6d28d9; /* Violet 700 */
            --primary-light: #ede9fe; /* Violet 100 */
            --secondary-color: #059669; /* Green 600 - for success states */
            --accent-color: #dc2626; /* Red 600 - for errors and highlights */
            --warning-color: #d97706; /* Orange 600 - for warnings */
            --text-primary: #1f2937; /* Gray 800 - high contrast text */
            --text-secondary: #4b5563; /* Gray 600 - secondary text */
            --text-muted: #6b7280; /* Gray 500 - muted text */
            --background-primary: #ffffff; /* White background */
            --background-secondary: #f9fafb; /* Gray 50 - subtle background */
            --background-accent: #f3f4f6; /* Gray 100 - accent background */
            --border-color: #e5e7eb; /* Gray 200 - subtle borders */
            --border-focus: #7c3aed; /* Primary color for focus states */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        /* Container */
        .main .block-container {
            max-width: 1100px;
            margin-left: auto;
            margin-right: auto;
            padding: 1.5rem 2rem;
            background-color: var(--background-primary);
            border-radius: 12px;
            box-shadow: var(--shadow-lg);
            border: 1px solid var(--border-color);
            font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
                 Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            color: var(--text-primary);
        }

        /* Headers with proper hierarchy and contrast (scoped to main content) */
        .main .block-container h1 {
            font-weight: 700;
            color: var(--text-primary);
            font-size: 2.5rem;
            margin-top: 0;
            margin-bottom: 1rem;
            letter-spacing: -0.025em;
            line-height: 1.2;
        }

        .main .block-container h2 {
            font-weight: 600;
            color: var(--primary-color);
            font-size: 2rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            letter-spacing: -0.025em;
            line-height: 1.3;
        }

        .main .block-container h3 {
            font-weight: 600;
            color: var(--text-primary);
            font-size: 1.5rem;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            line-height: 1.4;
        }

        .main .block-container h4 {
            font-weight: 600;
            color: var(--text-secondary);
            font-size: 1.25rem;
            margin-top: 1.25rem;
            margin-bottom: 0.5rem;
            line-height: 1.4;
        }

        /* Text readability with proper contrast */
        .main .block-container p, 
        .main .block-container li, 
        .stTextArea textarea {
            font-size: 1.125rem;
            line-height: 1.7;
            color: var(--text-primary);
        }

        /* Columns and layout spacing */
        [data-testid="stColumns"] > div {
            padding: 1.5rem;
            /* avoid painting theme backgrounds */
            background: transparent;
            border-radius: 12px;
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--border-color);
            transition: all 0.2s ease;
        }
        [data-testid="stColumns"] > div:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-1px);
        }

        /* Force Streamlit content containers to full width */
        .st-emotion-cache-1vr7d6u {
            width: 100% !important;
            max-width: 100% !important;
            min-width: 100% !important;
        }

        /* Buttons with accessible contrast and focus states */
        .stButton > button {
            background-color: var(--primary-color) !important;
            color: white !important;            
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 0.75rem 1.5rem !important;
            border: none !important;
            transition: all 0.2s ease !important;
            box-shadow: var(--shadow-sm) !important;
        }
        .stButton > button:hover {
            background-color: var(--primary-hover) !important;
            box-shadow: var(--shadow-md) !important;
            transform: translateY(-1px) !important;
        }
        .stButton > button:focus-visible {
            outline: 3px solid var(--primary-light) !important;
            outline-offset: 2px !important;
            box-shadow: 0 0 0 3px var(--primary-light) !important;
        }

        /* Secondary buttons */
        .st-emotion-cache-5qfegl {
            background-color: var(--background-secondary) !important;
            color: var(--primary-color) !important;            
            border: 2px solid var(--primary-color) !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 0.75rem 1.5rem !important;
            transition: all 0.2s ease !important;
        }
        .st-emotion-cache-5qfegl:hover {
            background-color: var(--primary-color) !important;
            color: white !important;
            border-color: var(--primary-color) !important;
        }
        .st-emotion-cache-5qfegl:focus-visible {
            outline: 3px solid var(--primary-light) !important;
            outline-offset: 2px !important;
        }

        /* Form elements with proper contrast */
        div[data-baseweb="radio"] label, 
        div[data-baseweb="checkbox"] label {
            color: var(--text-primary) !important; 
            font-weight: 500;
        }
        div[data-baseweb="radio"] input:checked + label::before, 
        div[data-baseweb="checkbox"] input:checked + label::before {
            background-color: var(--primary-color) !important;
            border-color: var(--primary-color) !important;
        }
        
        /* Metrics and status indicators (avoid repainting app chrome) */
        /* Remove background paints that darken main app */
        .st-av {
            background-color: transparent !important;
        }
        .st-cr {
            background-color: transparent !important;
        }
        
        /* Hyperlinks with proper contrast and focus states (scoped) */
        .main .block-container a {
            color: var(--primary-color);
            text-decoration: underline;
            text-decoration-thickness: 2px;
            text-underline-offset: 2px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .main .block-container a:hover { 
            color: var(--primary-hover);
            text-decoration-thickness: 3px;
        }
        .main .block-container a:focus-visible {
            outline: 3px solid var(--primary-light);
            outline-offset: 2px;
            border-radius: 4px;
            text-decoration: none;
        }

        /* Status messages with proper contrast */
        .stError { 
            color: var(--accent-color); 
            font-weight: 600; 
            background-color: #fef2f2;
            padding: 0.75rem;
            border-radius: 8px;
            border-left: 4px solid var(--accent-color);
        }
        .stWarning { 
            color: var(--warning-color); 
            font-weight: 600; 
            background-color: #fffbeb;
            padding: 0.75rem;
            border-radius: 8px;
            border-left: 4px solid var(--warning-color);
        }
        .stSuccess {
            color: var(--secondary-color);
            font-weight: 600;
            background-color: #f0fdf4;
            padding: 0.75rem;
            border-radius: 8px;
            border-left: 4px solid var(--secondary-color);
        }
        .stInfo {
            color: var(--primary-color);
            font-weight: 600;
            background-color: var(--primary-light);
            padding: 0.75rem;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
        }

        /* Focus management for accessibility */
        *:focus-visible {
            outline: 3px solid var(--primary-light);
            outline-offset: 2px;
            border-radius: 4px;
        }

        /* High contrast mode support */
        @media (prefers-contrast: high) {
            :root {
                --primary-color: #0000ff;
                --text-primary: #000000;
                --background-primary: #ffffff;
                --border-color: #000000;
            }
        }

        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }

        /* Dark mode support (if needed in future) */
        @media (prefers-color-scheme: dark) {
            :root {
                --text-primary: #f9fafb;
                --text-secondary: #d1d5db;
                --text-muted: #9ca3af;
                --background-primary: #111827;
                --background-secondary: #1f2937;
                --background-accent: #374151;
                --border-color: #374151;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
