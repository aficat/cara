import streamlit as st
from components.style import inject_custom_css
from components.layout import page_header, input_section, display_results
from components.pipeline import ask_cara_pipeline

def main():
    st.set_page_config(page_title="Ask CARA - CPF Content Assistant", layout="wide")
    inject_custom_css()
    page_header()

    content_input, page_type, run_button = input_section()

    if run_button and content_input:
        with st.spinner("🧠 CARA is thinking... this may take a few seconds"):
            try:
                result = ask_cara_pipeline(content_input, page_type)
                display_results(result)
                st.balloons()
            except Exception as e:
                st.error(f"⚠️ Something went wrong: {e}")
    else:
        st.caption("Paste content and hit the button above to start.")

if __name__ == "__main__":
    main()


# import streamlit as st
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
# from langchain.schema import HumanMessage
# from typing import Dict
# import json

# # Load OpenAI API Key securely from Streamlit Secrets
# openai_api_key = st.secrets["OPENAI_API_KEY"]

# # Set up the LLM (GPT-4 or fallback)
# llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key, temperature=0.3)

# # App title and description
# st.set_page_config(page_title="Ask CARA - CPF Content Assistant", layout="wide")
# st.title("Ask CARA 🧠")
# st.subheader("Content Assistant for Readable & Accessible content")

# st.markdown("""
# Ask CARA helps CPF product owners and content authors confidently create high-quality citizen-facing scheme and article pages.
# Paste your draft, choose the page type, and CARA will:
# - Recommend structure and headers
# - Rewrite content in CPF’s voice and hierarchy
# - Check for accessibility and SEO compliance
# - Generate a before/after governance report
# """)

# # --- Step 1: Input Section ---
# content_input = st.text_area("Paste your draft CPF scheme/article page here:", height=300)

# page_type = st.selectbox("Select type of page:", ["Scheme Info", "Application Guide", "Eligibility Criteria", "Others"])

# run_button = st.button("✨ Optimise with Ask CARA")

# # --- Step 2: Processing Logic ---
# def ask_cara_pipeline(raw_text: str, page_type: str) -> Dict:
#     prompt = f"""
# You are CARA, the CPF Content Assistant. Your job is to help content authors structure, rewrite, and improve CPF scheme/article pages.

# INPUT:
# - Page type: {page_type}
# - Draft content: {raw_text}

# TASKS:
# 1. Classify the content's intent.
# 2. Recommend a CPF-compliant page structure (e.g., Who it’s for, How to apply).
# 3. Rewrite and restructure the draft using CPF’s tone and content hierarchy (H1, H2, bullet points).
# 4. Perform WCAG 2.1 accessibility checks: fix unclear link text, missing alt text, heading hierarchy issues.
# 5. Perform SEO improvements: meaningful headings, internal link suggestions, keyword clarity.
# 6. Generate a Governance Report Card with: a summary of changes, structure compliance, tone alignment, accessibility and SEO improvements.

# Respond in the following JSON format:
# {
#   "intent": "...",
#   "recommended_structure": ["...", "..."],
#   "revised_content": "...",
#   "accessibility_fixes": ["..."],
#   "seo_fixes": ["..."],
#   "governance_report": {
#     "structure_score": "...",
#     "tone_score": "...",
#     "accessibility_score": "...",
#     "seo_score": "...",
#     "summary": "..."
#   }
# }
# """
#     response = llm([HumanMessage(content=prompt)])
#     return json.loads(response.content)

# # --- Step 3: Run and Display Results ---
# if run_button and content_input:
#     with st.spinner("CARA is thinking..."):
#         try:
#             result = ask_cara_pipeline(content_input, page_type)

#             st.success("Optimisation complete!")

#             st.markdown("### 🧭 Page Intent")
#             st.code(result['intent'], language='markdown')

#             st.markdown("### 🧱 Recommended Structure")
#             st.markdown("\n".join(f"- {h}" for h in result['recommended_structure']))

#             st.markdown("### ✍️ Revised Content")
#             st.text_area("Optimised Content:", result['revised_content'], height=300)

#             st.markdown("### ♿ Accessibility Fixes")
#             for fix in result['accessibility_fixes']:
#                 st.markdown(f"- {fix}")

#             st.markdown("### 🔍 SEO Fixes")
#             for fix in result['seo_fixes']:
#                 st.markdown(f"- {fix}")

#             st.markdown("### 📊 Governance Report Card")
#             st.metric("Structure Score", result['governance_report']['structure_score'])
#             st.metric("Tone Score", result['governance_report']['tone_score'])
#             st.metric("Accessibility Score", result['governance_report']['accessibility_score'])
#             st.metric("SEO Score", result['governance_report']['seo_score'])

#             st.markdown("#### Summary")
#             st.info(result['governance_report']['summary'])

#         except Exception as e:
#             st.error(f"Something went wrong: {e}")
# else:
#     st.caption("Paste content and hit the button above to start.")
