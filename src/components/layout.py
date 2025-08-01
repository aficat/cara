import streamlit as st

def page_header():
    st.title("Ask CARA 🧠")
    st.subheader("Content Assistant for Readable & Accessible content")
    st.markdown("""
    Ask CARA helps product owners and content authors confidently create high-quality citizen-facing scheme and article pages.
    Paste your draft, choose the page type, and CARA will:
    - Recommend structure and headers
    - Rewrite content in CPF’s voice and hierarchy
    - Check for accessibility and SEO compliance
    - Generate a before/after governance report
    """)

def input_section():
    col1, col2 = st.columns([2, 1])
    with col1:
        content_input = st.text_area("✍️ Paste your draft scheme/article page here:", height=300)
    with col2:
        page_type = st.selectbox("📄 Select type of page:", ["Scheme Info", "Application Guide", "Eligibility Criteria", "Others"])
        run_button = st.button("✨ Optimise with Ask CARA", use_container_width=True)
    return content_input, page_type, run_button

def display_results(result: dict):
    st.markdown("### 🧭 Page Intent")
    st.code(result.get('intent', 'N/A'), language='markdown')

    st.markdown("### 🧱 Recommended Structure")
    st.markdown("\n".join(f"- {h}" for h in result.get('recommended_structure', [])))

    st.markdown("### ✍️ Revised Content")
    st.text_area("Optimised Content:", result.get('revised_content', ''), height=300)

    st.markdown("### ♿ Accessibility Fixes")
    for fix in result.get('accessibility_fixes', []):
        st.markdown(f"- {fix}")

    st.markdown("### 🔍 SEO Fixes")
    for fix in result.get('seo_fixes', []):
        st.markdown(f"- {fix}")

    st.markdown("### 📊 Governance Report Card")
    scores = result.get('governance_report', {})
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Structure Score", scores.get('structure_score', 'N/A'))
    metric_col2.metric("Tone Score", scores.get('tone_score', 'N/A'))
    metric_col3.metric("Accessibility Score", scores.get('accessibility_score', 'N/A'))
    metric_col4.metric("SEO Score", scores.get('seo_score', 'N/A'))

    st.markdown("#### Summary")
    st.info(scores.get('summary', ''))
