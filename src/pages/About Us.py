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
    - Uses **OpenAI large language models** for advanced content analysis and rewriting.
    - Relies on the **Content playbook** document for governance and style rules.
    - Follows **accessibility standards** based on the [WCAG 2.1 guidelines](https://www.w3.org/WAI/WCAG21/) and incorporates audits inspired by [Lighthouse Accessibility Scoring](https://developer.chrome.com/docs/lighthouse/accessibility/scoring).
    - Implements **SEO best practices** guided by Google's [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide), along with audits for descriptive link text, meta descriptions, and font size legibility using [Lighthouse SEO audits](https://developer.chrome.com/docs/lighthouse/seo/link-text), [meta description checks](https://developer.chrome.com/docs/lighthouse/seo/meta-description), and [font size guidelines](https://developer.chrome.com/docs/lighthouse/seo/font-size).

    ### Features
    - Content input via URL, text, or document upload.
    - Automated content rewriting with tone, structure, accessibility, and SEO guidance.
    - Governance report card with scores.
    - Side-by-side comparison of original and improved content.
    - Download options for revised content.

    ### Learn more about Accessibility
    Visit [web.dev's accessibility learning resources](https://web.dev/learn/accessibility) to deepen your understanding of accessibility principles.
    """)

if __name__ == "__main__":
    about_us()