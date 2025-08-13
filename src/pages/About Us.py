import streamlit as st

def about_us():
    st.title("About Us")
    
    st.markdown("""
    ### Project Scope
    This project aims to provide users with a comprehensive content review assistant to improve clarity, accessibility, and SEO compliance.
    
    ### Objectives
    - Assist public officers in producing accessible and citizen-friendly web content.
    - Streamline content governance using AI-powered suggestions.
    - Enhance consistency and user experience across digital content.
    
    ### Data Sources
    - Government content playbook PDF documents.
    - Publicly available gov.sg webpages.
    - OpenAI large language models for content analysis.
    
    ### Features
    - Content input via URL, text, or document upload.
    - Automated content rewriting with tone, structure, accessibility, and SEO guidance.
    - Governance report card with scores.
    - Side-by-side comparison of original and improved content.
    - Download options for revised content.
    """)

if __name__ == "__main__":
    about_us()