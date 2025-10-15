from components.style import inject_custom_css
from components.layout import add_sidebar_copyright
import streamlit as st

inject_custom_css()

def about_us():
    st.title("About Us")
    
    # Add sidebar copyright at the bottom left
    add_sidebar_copyright()
    
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

    ### Sample data inputs
    - Webpage URL: https://www.cpf.gov.sg/member/healthcare-financing/about-health-insurance-planner
    - Paste draft text directly: Draft text.md under samples folder
    - Word document upload: Word document sample.docx under samples folder
                
    ### Sample data outputs
    - Word document: CARAble Content Revision.docx under samples folder
    - HTML file: CARAble Content Revision.html under samples folder

    ### Learn more about Accessibility
    Visit [web.dev's accessibility learning resources](https://web.dev/learn/accessibility) to deepen your understanding of accessibility principles.
    """)

    st.image("src/samples/Carable screenshot 1.png", caption="Screenshot of CARAble interface 1")
    st.image("src/samples/Carable screenshot 1.png", caption="Screenshot of CARAble interface 2")

if __name__ == "__main__":
    about_us()