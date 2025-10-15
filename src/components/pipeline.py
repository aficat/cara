import json
import os
import re
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import UnstructuredWordDocumentLoader
import nltk
from components.style import inject_custom_css
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
from bs4 import BeautifulSoup
import textstat


# Load API key from Streamlit Secrets
openai_api_key = st.secrets["api"]["OPENAI_API_KEY"]

# Load API key from .env
# from dotenv import load_dotenv
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("vader_lexicon")

inject_custom_css()

# -----------------------------
# Data Classes for Content Analysis
# -----------------------------
@dataclass
class ContentMetrics:
    """Structured metrics for content analysis"""
    readability_score: float
    word_count: int
    sentence_count: int
    paragraph_count: int
    heading_count: int
    link_count: int
    image_count: int
    accessibility_issues: List[str]
    seo_issues: List[str]
    tone_issues: List[str]
    structure_issues: List[str]

@dataclass
class GovernanceScore:
    """Structured governance scoring"""
    structure_score: float
    tone_score: float
    accessibility_score: float
    seo_score: float
    overall_score: float
    confidence_level: str

# -----------------------------
# Enhanced Content Analysis Functions
# -----------------------------
def analyze_content_structure(content: str) -> Dict:
    """Analyze content structure and hierarchy"""
    soup = BeautifulSoup(content, 'html.parser')
    
    # Count structural elements
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    paragraphs = soup.find_all('p')
    lists = soup.find_all(['ul', 'ol'])
    links = soup.find_all('a')
    images = soup.find_all('img')
    
    # Analyze heading hierarchy
    heading_hierarchy = []
    for heading in headings:
        level = int(heading.name[1])
        heading_hierarchy.append({
            'level': level,
            'text': heading.get_text().strip(),
            'length': len(heading.get_text().strip())
        })
    
    # Check for proper heading sequence and structure
    structure_issues = []
    if heading_hierarchy:
        prev_level = 0
        for heading in heading_hierarchy:
            if heading['level'] > prev_level + 1:
                structure_issues.append(f"Missing heading level between H{prev_level} and H{heading['level']}")
            prev_level = heading['level']
    
    # Check for missing H1
    h1_count = len([h for h in headings if h.name == 'h1'])
    if h1_count == 0:
        structure_issues.append("Missing H1 heading for main title")
    
    # Check for H2 usage (main sections)
    h2_count = len([h for h in headings if h.name == 'h2'])
    if h2_count == 0 and len(headings) > 1:
        structure_issues.append("Missing H2 headings for main sections")
    
    # Check for H3 usage (subsections)
    h3_count = len([h for h in headings if h.name == 'h3'])
    if h3_count == 0 and len(headings) > 2:
        structure_issues.append("Consider using H3 headings for subsections")
    
    # Check for content length
    if len(paragraphs) < 2:
        structure_issues.append("Insufficient content structure (less than 2 paragraphs)")
    
    return {
        'heading_count': len(headings),
        'h1_count': h1_count,
        'h2_count': h2_count,
        'h3_count': h3_count,
        'paragraph_count': len(paragraphs),
        'list_count': len(lists),
        'link_count': len(links),
        'image_count': len(images),
        'heading_hierarchy': heading_hierarchy,
        'structure_issues': structure_issues
    }

def analyze_accessibility(content: str) -> List[str]:
    """Enhanced accessibility analysis for WCAG 2.1 AA compliance"""
    soup = BeautifulSoup(content, 'html.parser')
    issues = []
    
    # Check for missing alt text on images
    images = soup.find_all('img')
    for img in images:
        if not img.get('alt'):
            issues.append("Image missing alt text for accessibility")
        elif img.get('alt').strip() == '':
            issues.append("Image has empty alt text - should be descriptive or empty for decorative images")
    
    # Check for descriptive link text
    links = soup.find_all('a')
    for link in links:
        link_text = link.get_text().strip()
        href = link.get('href', '')
        if link_text in ['click here', 'read more', 'here', 'more', 'link', 'this']:
            issues.append(f"Link text '{link_text}' is not descriptive enough")
        if href and not link_text:
            issues.append("Link missing descriptive text")
        if href and len(link_text) < 3:
            issues.append("Link text too short - should be at least 3 characters")
    
    # Enhanced heading hierarchy analysis
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    if headings:
        levels = [int(h.name[1]) for h in headings]
        if 1 not in levels and 2 not in levels:
            issues.append("Content should start with H1 or H2 heading")
        
        # Check for heading level skipping
        for i in range(1, len(levels)):
            if levels[i] > levels[i-1] + 1:
                issues.append(f"Heading level skipped from H{levels[i-1]} to H{levels[i]}")
        
        # Check for multiple H1s
        h1_count = levels.count(1)
        if h1_count > 1:
            issues.append(f"Multiple H1 headings found ({h1_count}) - should only have one")
    
    # Check for colour contrast issues (basic check)
    style_tags = soup.find_all('style')
    for style in style_tags:
        if style.string and 'color:' in style.string and 'background-color:' not in style.string:
            issues.append("Text colour specified without background colour - may cause contrast issues")
    
    # Check for form accessibility
    forms = soup.find_all('form')
    for form in forms:
        inputs = form.find_all(['input', 'textarea', 'select'])
        for input_elem in inputs:
            if input_elem.get('type') not in ['hidden', 'submit', 'button']:
                label = form.find('label', {'for': input_elem.get('id')})
                if not label and not input_elem.get('aria-label'):
                    issues.append("Form input missing label or aria-label")
    
    # Check for table accessibility
    tables = soup.find_all('table')
    for table in tables:
        if not table.find('caption') and not table.get('aria-label'):
            issues.append("Table missing caption or aria-label")
        
        # Check for proper table headers
        headers = table.find_all(['th'])
        if not headers:
            issues.append("Table missing header cells (th elements)")
    
    return issues

def analyze_seo(content: str) -> List[str]:
    """Analyze content for SEO best practices"""
    soup = BeautifulSoup(content, 'html.parser')
    issues = []
    
    # Check for meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if not meta_desc:
        issues.append("Missing meta description for SEO")
    elif meta_desc.get('content'):
        desc_length = len(meta_desc.get('content'))
        if desc_length < 120:
            issues.append("Meta description too short (should be 120-160 characters)")
        elif desc_length > 160:
            issues.append("Meta description too long (should be 120-160 characters)")
    
    # Check heading structure for keywords
    headings = soup.find_all(['h1', 'h2', 'h3'])
    if not headings:
        issues.append("Content should have proper heading structure for SEO")
    
    # Check for internal linking
    links = soup.find_all('a')
    internal_links = [link for link in links if link.get('href', '').startswith('/') or 'gov.sg' in link.get('href', '')]
    if len(internal_links) < 2:
        issues.append("Consider adding more internal links for better SEO")
    
    # Check paragraph length
    paragraphs = soup.find_all('p')
    long_paragraphs = [p for p in paragraphs if len(p.get_text()) > 200]
    if len(long_paragraphs) > len(paragraphs) * 0.5:
        issues.append("Too many long paragraphs - consider breaking them up for better readability")
    
    return issues

def analyze_readability(content: str) -> Dict:
    """Analyze content readability using multiple metrics"""
    # Extract plain text for analysis
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    
    # Calculate readability scores
    flesch_score = textstat.flesch_reading_ease(text)
    flesch_kincaid = textstat.flesch_kincaid_grade(text)
    gunning_fog = textstat.gunning_fog(text)
    
    # Word and sentence counts
    word_count = textstat.lexicon_count(text)
    sentence_count = textstat.sentence_count(text)
    
    # Determine readability level
    if flesch_score >= 80:
        readability_level = "Very Easy"
    elif flesch_score >= 60:
        readability_level = "Easy"
    elif flesch_score >= 30:
        readability_level = "Moderate"
    else:
        readability_level = "Difficult"
    
    return {
        'flesch_score': flesch_score,
        'flesch_kincaid_grade': flesch_kincaid,
        'gunning_fog': gunning_fog,
        'word_count': word_count,
        'sentence_count': sentence_count,
        'readability_level': readability_level
    }

# -----------------------------
# Load Content Playbook
# -----------------------------
@st.cache_resource
def load_content_playbook():
    loader = UnstructuredWordDocumentLoader("src/resources/contentplaybook.docx")
    docs = loader.load()
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

# -----------------------------
# CARAble LLM initialization
# -----------------------------
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    openai_api_key=openai_api_key,
    temperature=0.1
)

MAX_CHARS = 15000  # Increased for article-sized content processing

# -----------------------------
# Utility functions
# -----------------------------
def clean_response(raw_text: str) -> str:
    """Remove control characters from raw model output (except \n, \t) and retain the heading types if any."""
    return re.sub(r'[\x00-\x1f\x7f]', '', raw_text)

def truncate_text(text: str, max_chars=MAX_CHARS) -> str:
    """Truncate text to max_chars while preserving line breaks and content structure."""
    if len(text) <= max_chars:
        return text

    # Try to truncate at a natural break point (paragraph or heading)
    truncated = ""
    current_length = 0
    
    # Split by double line breaks (paragraphs) first
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        if current_length + len(paragraph) + 2 <= max_chars:  # +2 for \n\n
            truncated += paragraph + '\n\n'
            current_length += len(paragraph) + 2
        else:
            # If this paragraph would exceed limit, try to truncate within it
            remaining = max_chars - current_length - 50  # Leave room for truncation notice
            if remaining > 100:  # Only if we have meaningful space left
                # Try to find a sentence break
                sentences = paragraph.split('. ')
                for sentence in sentences:
                    if current_length + len(sentence) + 2 <= max_chars - 50:
                        truncated += sentence + '. '
                        current_length += len(sentence) + 2
                    else:
                        break
            break
    
    # If we still haven't used much space, fall back to line-by-line truncation
    if len(truncated) < max_chars * 0.5:
        truncated = ""
        for line in text.splitlines(True):
            if len(truncated) + len(line) > max_chars - 50:
                remaining = max_chars - len(truncated) - 50
                truncated += line[:remaining]
                break
            truncated += line

    # Return truncated content without adding any truncation notice
    return truncated.rstrip()


# -----------------------------
# Guideline links for LLM reference
# -----------------------------
guideline_links = """
Accessibility references:
- WCAG 2.1 guidelines: https://www.w3.org/WAI/WCAG21/
- Lighthouse Accessibility Scoring: https://developer.chrome.com/docs/lighthouse/accessibility/scoring/

SEO references:
- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Lighthouse SEO audits: https://developer.chrome.com/docs/lighthouse/seo/link-text
- Meta description checks: https://developer.chrome.com/docs/lighthouse/seo/meta-description
- Font size guidelines: https://developer.chrome.com/docs/lighthouse/seo/font-size
"""

# -----------------------------
# Enhanced Scoring Functions
# -----------------------------
def calculate_governance_scores(content: str, content_metrics: ContentMetrics) -> GovernanceScore:
    """Calculate comprehensive governance scores based on content analysis with detailed penalty system"""
    
    # Structure Score (0-10) - More granular scoring
    structure_score = 10.0
    structure_penalties = 0
    
    # Heading issues
    if content_metrics.heading_count == 0:
        structure_penalties += 4.0  # Major penalty for no headings
    elif content_metrics.heading_count < 2:
        structure_penalties += 2.0  # Penalty for insufficient headings
    
    # Structure issues from analysis
    structure_penalties += len(content_metrics.structure_issues) * 1.5
    
    # Content length issues
    if content_metrics.paragraph_count < 2:
        structure_penalties += 2.0
    elif content_metrics.paragraph_count < 3:
        structure_penalties += 1.0
    
    structure_score = max(0, structure_score - structure_penalties)
    structure_score = round(structure_score)  # Round to whole number
    
    # Accessibility Score (0-10) - Detailed penalty system
    accessibility_score = 10.0
    accessibility_penalties = 0
    
    # Count specific accessibility issues
    alt_text_issues = sum(1 for issue in content_metrics.accessibility_issues if "alt text" in issue.lower())
    link_issues = sum(1 for issue in content_metrics.accessibility_issues if "link" in issue.lower())
    heading_issues = sum(1 for issue in content_metrics.accessibility_issues if "heading" in issue.lower())
    
    accessibility_penalties += alt_text_issues * 2.0  # High penalty for missing alt text
    accessibility_penalties += link_issues * 1.5     # Medium penalty for link issues
    accessibility_penalties += heading_issues * 1.0  # Lower penalty for heading issues
    accessibility_penalties += (len(content_metrics.accessibility_issues) - alt_text_issues - link_issues - heading_issues) * 1.0
    
    accessibility_score = max(0, accessibility_score - accessibility_penalties)
    accessibility_score = round(accessibility_score)  # Round to whole number
    
    # SEO Score (0-10) - Detailed penalty system
    seo_score = 10.0
    seo_penalties = 0
    
    # Count specific SEO issues
    meta_issues = sum(1 for issue in content_metrics.seo_issues if "meta" in issue.lower())
    heading_seo_issues = sum(1 for issue in content_metrics.seo_issues if "heading" in issue.lower())
    link_seo_issues = sum(1 for issue in content_metrics.seo_issues if "link" in issue.lower())
    
    seo_penalties += meta_issues * 2.5  # High penalty for meta description issues
    seo_penalties += heading_seo_issues * 1.5  # Medium penalty for heading SEO issues
    seo_penalties += link_seo_issues * 1.0  # Lower penalty for link SEO issues
    seo_penalties += (len(content_metrics.seo_issues) - meta_issues - heading_seo_issues - link_seo_issues) * 1.0
    
    # Additional SEO penalties
    if content_metrics.link_count < 2:
        seo_penalties += 1.5
    if content_metrics.heading_count < 2:
        seo_penalties += 1.0
    
    seo_score = max(0, seo_score - seo_penalties)
    seo_score = round(seo_score)  # Round to whole number
    
    # Tone Score (0-10) - Based on readability and content quality
    tone_score = 10.0
    tone_penalties = 0
    
    # Readability penalties
    if content_metrics.readability_score < 30:  # Very difficult to read
        tone_penalties += 4.0
    elif content_metrics.readability_score < 50:  # Difficult to read
        tone_penalties += 2.5
    elif content_metrics.readability_score < 70:  # Moderate difficulty
        tone_penalties += 1.0
    
    # Content length penalties
    if content_metrics.word_count < 100:
        tone_penalties += 2.0  # Too short
    elif content_metrics.word_count < 200:
        tone_penalties += 1.0  # Somewhat short
    
    # Sentence structure penalties
    if content_metrics.sentence_count > 0:
        avg_words_per_sentence = content_metrics.word_count / content_metrics.sentence_count
        if avg_words_per_sentence > 25:  # Very long sentences
            tone_penalties += 2.0
        elif avg_words_per_sentence > 20:  # Long sentences
            tone_penalties += 1.0
    
    tone_score = max(0, tone_score - tone_penalties)
    tone_score = round(tone_score)  # Round to whole number
    
    # Overall Score
    overall_score = (structure_score + accessibility_score + seo_score + tone_score) / 4
    overall_score = round(overall_score)  # Round to whole number
    
    # Confidence Level based on consistency
    score_variance = max([structure_score, accessibility_score, seo_score, tone_score]) - min([structure_score, accessibility_score, seo_score, tone_score])
    if overall_score >= 8.0 and score_variance <= 2.0:
        confidence_level = "High"
    elif overall_score >= 6.0 and score_variance <= 4.0:
        confidence_level = "Medium"
    else:
        confidence_level = "Low"
    
    return GovernanceScore(
        structure_score=round(structure_score, 1),
        tone_score=round(tone_score, 1),
        accessibility_score=round(accessibility_score, 1),
        seo_score=round(seo_score, 1),
        overall_score=round(overall_score, 1),
        confidence_level=confidence_level
    )

def get_page_type_guidelines(page_type: str) -> str:
    """Get page type specific guidelines for enhanced content governance"""
    guidelines = {
        "article": """
        - Use clear, descriptive headlines (H1)
        - Include executive summary or key takeaways
        - Structure with logical subheadings (H2, H3)
        - Include relevant internal and external links
        - End with clear call-to-action or next steps
        """,
        "service": """
        - Start with what the service is and who it's for
        - Include eligibility criteria and requirements
        - Provide step-by-step instructions
        - List required documents and fees
        - Include contact information and support
        """,
        "policy": """
        - Use formal, authoritative tone
        - Include policy number and effective date
        - Structure with clear sections and subsections
        - Include definitions of key terms
        - Provide contact for questions or clarifications
        """,
        "news": """
        - Use inverted pyramid structure
        - Include who, what, when, where, why in first paragraph
        - Use active voice and present tense
        - Include relevant quotes and statistics
        - End with background context if needed
        """
    }
    return guidelines.get(page_type.lower(), "Follow general content governance principles.")

def generate_detailed_analysis(content: str) -> ContentMetrics:
    """Generate comprehensive content analysis with enhanced metrics"""
    structure_analysis = analyze_content_structure(content)
    accessibility_issues = analyze_accessibility(content)
    seo_issues = analyze_seo(content)
    readability_analysis = analyze_readability(content)
    
    return ContentMetrics(
        readability_score=readability_analysis['flesch_score'],
        word_count=readability_analysis['word_count'],
        sentence_count=readability_analysis['sentence_count'],
        paragraph_count=structure_analysis['paragraph_count'],
        heading_count=structure_analysis['heading_count'],
        link_count=structure_analysis['link_count'],
        image_count=structure_analysis['image_count'],
        accessibility_issues=accessibility_issues,
        seo_issues=seo_issues,
        tone_issues=[],  # Will be filled by LLM analysis
        structure_issues=structure_analysis['structure_issues']
    )

# -----------------------------
# Enhanced CARAble Pipeline
# -----------------------------
def ask_cara_pipeline(raw_text: str, page_type: str) -> dict:
    """Advanced CARAble pipeline with multi-agent content governance system.
    
    This function provides enterprise-grade content governance by:
    - Preserve headings, paragraphs, bullets, tables
    - Apply content playbook, WCAG, and SEO checks
    - Output JSON with revised content and report card
    - Multi-dimensional content analysis with AI reasoning
    - Context-aware content playbook integration
    - Dynamic scoring with confidence intervals
    - Actionable recommendations with implementation priority
    - Content enhancement suggestions with alternatives
    """
    
    # Perform comprehensive content analysis
    content_metrics = generate_detailed_analysis(raw_text)
    governance_scores = calculate_governance_scores(raw_text, content_metrics)
    
    # Prepare content for LLM processing (avoid aggressive truncation)
    truncated_text = raw_text if len(raw_text) <= MAX_CHARS else truncate_text(raw_text)
    vectorstore = load_content_playbook()

    # Enhanced content playbook retrieval with context awareness
    related_guidelines = vectorstore.similarity_search(truncated_text, k=10)
    guidelines_text = "\n".join([doc.page_content for doc in related_guidelines])
    
    # Add content type specific guidelines
    page_type_guidelines = get_page_type_guidelines(page_type)
    all_guidelines = f"{guidelines_text}\n\nPAGE TYPE SPECIFIC GUIDELINES:\n{page_type_guidelines}"

    # Enhanced prompt focused on content corrections and improvements
    prompt = f"""
You are CARAble, an advanced Content Governance Assistant specialising in content corrections and compliance.

DETECTED ISSUES FROM ANALYSIS:
- Structure Issues: {content_metrics.structure_issues}
- Accessibility Issues: {content_metrics.accessibility_issues}
- SEO Issues: {content_metrics.seo_issues}
- Readability Score: {content_metrics.readability_score:.1f} (Flesch Reading Ease)
- Word Count: {content_metrics.word_count}
- Heading Count: {content_metrics.heading_count}
- Link Count: {content_metrics.link_count}

CONTENT PLAYBOOK GUIDELINES:
{all_guidelines}

EXTERNAL STANDARDS:
{guideline_links}

INPUT CONTENT:
- Page Type: {page_type}
- Content: {truncated_text}

CONTENT CORRECTION & IMPROVEMENT REQUIREMENTS:

1. **CONTENT STRUCTURE FIXES**:
   - Fix heading hierarchy: H1 for main title, H2 for main sections, H3 for subsections
   - Suggest specific heading corrections: "Change 'Current heading' to 'H2: Corrected heading'"
   - Fix heading formatting and structure issues
   - Ensure logical flow: H1 → H2 → H3 → H4
   - Preserve original content structure while fixing hierarchy

2. **CONTENT PLAYBOOK COMPLIANCE FIXES**:
   - Fix terminology to match Content Playbook standards
   - Correct acronym usage (e.g., "CPF" not "Central Provident Fund" on first use)
   - Fix date formatting (e.g., "15 March 2024" not "March 15, 2024")
   - Correct spelling and grammar according to Content Playbook
   - Fix tone and voice inconsistencies
   - Preserve original meaning while fixing compliance issues

3. **WCAG 2.1 ACCESSIBILITY FIXES**:
   - Fix heading hierarchy violations
   - Add missing alt text for images
   - Fix descriptive link text issues
   - Simplify complex language where needed
   - Fix contrast and navigation issues
   - Address specific WCAG 2.1 AA compliance violations

4. **SEO COMPLIANCE FIXES**:
   - Fix keyword usage in headings
   - Improve meta descriptions
   - Fix internal linking structure
   - Address font size and mobile readability issues
   - Fix Google SEO Starter Guide violations
   - Address Lighthouse SEO audit issues

5. **GOVERNANCE REPORT CARD**:
   - Structure, tone, accessibility, and SEO scores (format: score/10)
   - Specific fixes with exact before/after examples
   - Highlight only the corrections made to original content

CRITICAL INSTRUCTIONS:
1. **PRESERVE ORIGINAL STRUCTURE**: Keep the exact same content structure, numbering, and formatting as the input. Only make targeted corrections for specific compliance issues.
2. **SCORING ALIGNMENT**: Your suggestions MUST directly correspond to the detected issues above. The number of suggestions should match the severity of issues found.
3. **SPECIFIC DETAILS**: Each suggestion must be specific, actionable, and include:
   - Exact location of the problem
   - Specific text that needs changing
   - Exact replacement text or action
   - Why the change is needed
4. **SCORE CONSISTENCY**: 
   - If a category has a perfect score (10/10), provide NO suggestions
   - If a category has a high score (8-9/10), provide 1-2 minor suggestions
   - If a category has a medium score (6-7/10), provide 3-4 specific suggestions
   - If a category has a low score (0-5/10), provide 5+ detailed suggestions
   - All scores must be whole numbers (e.g., 7/10, not 7.3/10)
5. **NO MAJOR REFORMATTING**: Do not change the overall structure, numbering system, or layout. Only fix specific compliance issues.

ANALYSIS REQUIREMENTS:
1. **Structure Analysis**:
   - ONLY suggest fixes for the detected structure issues: {content_metrics.structure_issues}
   - If no structure issues detected, provide NO structure suggestions
   - Each suggestion must specify exact heading changes needed

2. **Accessibility Analysis**:
   - ONLY suggest fixes for detected accessibility issues: {content_metrics.accessibility_issues}
   - If no accessibility issues detected, provide NO accessibility suggestions
   - Each suggestion must specify exact HTML changes needed

3. **SEO Analysis**:
   - ONLY suggest fixes for detected SEO issues: {content_metrics.seo_issues}
   - If no SEO issues detected, provide NO SEO suggestions
   - Each suggestion must specify exact meta tags or content changes needed

4. **Tone Analysis**:
   - Base suggestions on readability score: {content_metrics.readability_score:.1f}
   - If readability is good (70+), provide NO tone suggestions
   - If readability is poor, suggest specific sentence simplifications

OUTPUT REQUIREMENTS:
- PRESERVE ALL ORIGINAL CONTENT STRUCTURE - no omissions, summarisation, or major reformatting
- Keep original numbering format (1, 2, 3) - do NOT change to tick icons or bullets
- Maintain original heading hierarchy and structure exactly as provided
- Keep original paragraph breaks and formatting
- Only make targeted corrections for specific issues found
- Maintain similar word count to original
- Use proper HTML structure with headings, paragraphs, lists, hyperlinks, tables, bullets
- Remove elements: "script", "nav", "footer", "header", "noscript", "form", "img", "button", "input", "select"
- Return only valid JSON with string or string-array values
- Inputs and outputs in textual HTML formats (no markdown)
- Highlight only the specific corrections made to original content
- ONLY provide suggestions for categories with detected issues
- Each suggestion must be specific and actionable
- If no issues detected in a category, return empty array for that category
- DO NOT reformat the entire content - only fix specific compliance issues

OUTPUT FORMAT (JSON only):
{{
  "recommended_structure": ["H2: Main Topic", "H3: Sub-topic 1", "H3: Sub-topic 2"],
  "revised_content": "<h2>Main Topic</h2><p>Revised content...</p>",
  "accessibility_fixes": ["Specific fix with exact location and replacement", "Another specific fix"],
  "seo_fixes": ["Specific SEO fix with exact changes needed", "Another specific SEO fix"],
  "tone_fixes": ["Specific tone improvement with exact text changes", "Another specific tone fix"],
  "structure_fixes": ["Specific structure fix with exact heading changes", "Another specific structure fix"],
  "governance_report": {{
    "structure_score": "{governance_scores.structure_score}/10",
    "tone_score": "{governance_scores.tone_score}/10", 
    "accessibility_score": "{governance_scores.accessibility_score}/10",
    "seo_score": "{governance_scores.seo_score}/10",
    "overall_score": "{governance_scores.overall_score}/10",
    "confidence_level": "{governance_scores.confidence_level}",
    "summary": "Summary with specific before/after examples of major improvements",
    "before_after_comparison": ["Before: [specific text] → After: [improved text]", "Another example"]
  }}
}}"""
    
    try:
        response = llm([
            SystemMessage(content="You are CARAble, an expert Content Governance Assistant that preserves original content structure while making targeted compliance corrections. You focus on fixing specific issues rather than rewriting content."),
            HumanMessage(content=prompt)
        ])
        
        cleaned = clean_response(response.content)
        
        # Parse JSON response
        result = json.loads(cleaned)

        # Ensure revised_content always returns full content length where possible
        revised = result.get("revised_content")
        if not revised or len(revised.strip()) == 0:
            result["revised_content"] = raw_text

        # Post-process structure suggestions to be layman-friendly (H1/H2/H3... labels, no code)
        if "recommended_structure" in result and isinstance(result["recommended_structure"], list):
            layman_structure = []
            for item in result["recommended_structure"]:
                text = str(item)
                # Normalise to formats like "H1: Title" without markdown/code
                text = text.replace("# ", "H1: ").replace("## ", "H2: ").replace("### ", "H3: ")
                text = text.replace("<h1>", "H1: ").replace("</h1>", "")
                text = text.replace("<h2>", "H2: ").replace("</h2>", "")
                text = text.replace("<h3>", "H3: ").replace("</h3>", "")
                text = text.strip()
                layman_structure.append(text)
            result["recommended_structure"] = layman_structure

        # If any category score is below 10, ensure there are corresponding suggestions
        gr = result.get("governance_report", {})
        def parse_score(s):
            try:
                return int(str(s).split("/")[0])
            except Exception:
                return None
        structure_s = parse_score(gr.get("structure_score"))
        tone_s = parse_score(gr.get("tone_score"))
        access_s = parse_score(gr.get("accessibility_score"))
        seo_s = parse_score(gr.get("seo_score"))

        # Initialise arrays if missing
        for key in ["structure_fixes", "tone_fixes", "accessibility_fixes", "seo_fixes"]:
            if key not in result or not isinstance(result.get(key), list):
                result[key] = []

        if structure_s is not None and structure_s < 10 and len(result["structure_fixes"]) == 0:
            result["structure_fixes"].append("Provide at least one structure fix aligned to detected issues.")
        if tone_s is not None and tone_s < 10 and len(result["tone_fixes"]) == 0:
            result["tone_fixes"].append("Provide at least one tone/style fix aligned to readability and playbook.")
        if access_s is not None and access_s < 10 and len(result["accessibility_fixes"]) == 0:
            result["accessibility_fixes"].append("Provide at least one WCAG-related fix (e.g., headings, link text, alt text).")
        if seo_s is not None and seo_s < 10 and len(result["seo_fixes"]) == 0:
            result["seo_fixes"].append("Provide at least one SEO fix (meta description, headings, internal links).")
        
        # Enhance result with calculated scores if LLM scores are missing
        if "governance_report" not in result:
            result["governance_report"] = {}
        
        # Use calculated scores as fallback
        governance_report = result["governance_report"]
        if "structure_score" not in governance_report:
            governance_report["structure_score"] = f"{governance_scores.structure_score}/10"
        if "tone_score" not in governance_report:
            governance_report["tone_score"] = f"{governance_scores.tone_score}/10"
        if "accessibility_score" not in governance_report:
            governance_report["accessibility_score"] = f"{governance_scores.accessibility_score}/10"
        if "seo_score" not in governance_report:
            governance_report["seo_score"] = f"{governance_scores.seo_score}/10"
        if "overall_score" not in governance_report:
            governance_report["overall_score"] = f"{governance_scores.overall_score}/10"
        if "confidence_level" not in governance_report:
            governance_report["confidence_level"] = governance_scores.confidence_level
        
        # Add detailed analysis results
        result["detailed_analysis"] = {
            "accessibility_issues": content_metrics.accessibility_issues,
            "seo_issues": content_metrics.seo_issues,
            "structure_issues": content_metrics.structure_issues,
            "readability_analysis": {
                "flesch_score": content_metrics.readability_score,
                "word_count": content_metrics.word_count,
                "sentence_count": content_metrics.sentence_count,
                "readability_level": "Easy" if content_metrics.readability_score >= 60 else "Moderate" if content_metrics.readability_score >= 30 else "Difficult"
            }
        }
        
        return result
        
    except json.JSONDecodeError as e:
        # Fallback response if JSON parsing fails
        return {
            "recommended_structure": ["Content structure analysis failed"],
            "revised_content": raw_text,
            "accessibility_fixes": content_metrics.accessibility_issues,
            "seo_fixes": content_metrics.seo_issues,
            "tone_fixes": ["Tone analysis failed"],
            "structure_fixes": content_metrics.structure_issues,
            "governance_report": {
                "structure_score": f"{governance_scores.structure_score}/10",
                "tone_score": f"{governance_scores.tone_score}/10",
                "accessibility_score": f"{governance_scores.accessibility_score}/10",
                "seo_score": f"{governance_scores.seo_score}/10",
                "overall_score": f"{governance_scores.overall_score}/10",
                "confidence_level": governance_scores.confidence_level,
                "summary": "Analysis completed with calculated scores",
                "critical_issues": content_metrics.accessibility_issues + content_metrics.seo_issues,
                "next_steps": ["Review accessibility issues", "Address SEO recommendations"]
            },
            "detailed_analysis": {
                "accessibility_issues": content_metrics.accessibility_issues,
                "seo_issues": content_metrics.seo_issues,
                "structure_issues": content_metrics.structure_issues,
                "readability_analysis": {
                    "flesch_score": content_metrics.readability_score,
                    "word_count": content_metrics.word_count,
                    "sentence_count": content_metrics.sentence_count,
                    "readability_level": "Easy" if content_metrics.readability_score >= 60 else "Moderate" if content_metrics.readability_score >= 30 else "Difficult"
                }
            }
        }