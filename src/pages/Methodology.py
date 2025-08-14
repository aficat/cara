from components.style import inject_custom_css
import streamlit as st

inject_custom_css()

def methodology():
    st.title("Methodology")
    
    st.markdown("""
    ### Data flow and implementation details
    
    Our application focuses on three input use cases where users provide content via:
    - **Website URL** (gov.sg pages only)
    - **Pasted text** directly into the input box
    - **Uploading a Word Document** (.docx)
    
    Regardless of input method, the content undergoes the same processing pipeline:
    
    1. Content is fetched, extracted, or read based on the input type.
    2. The text content is sent to the CARAble pipeline leveraging OpenAI models for analysis.
    3. CARAble returns a detailed JSON response including content quality scores, suggestions, and rewritten content.
    4. The app displays:
       - Content scorecards for structure, tone, accessibility, and SEO.
       - Detailed improvement suggestions.
       - Side-by-side comparison of original and revised content.
       - Options to download the improved content as HTML or Word document.
    """)
    
    # Embed or link to the flowchart here
    st.markdown("#### Flowchart")

    st.markdown("The following flowchart illustrates this data flow and user journey across the input and output stages.")
    st.image("src/documentation/CARA Flowchart.png", caption="Flowchart")

if __name__ == "__main__":
    methodology()