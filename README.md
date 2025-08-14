# 🧠 CARAble – Content Authoring & Reviewing Assistant
Designed and developed by **Afiqah Rashid**

CARAble is an AI-powered assistant that helps content creators and reviewers generate, refine, and structure content efficiently. It provides an intuitive interface for drafting, improving, and validating content.

---

## 🛠️ Built with
- Python 3.8+  
- Streamlit  
- OpenAI API  

---

## 📌 Project Scope
This project aims to provide users with a comprehensive content review assistant to improve clarity, accessibility, and SEO compliance.

---

## 🎯 Objectives
- Assist public officers in producing accessible and citizen-friendly web content.  
- Streamline content governance using AI-powered suggestions.  
- Enhance consistency and user experience across digital content.

---

## ✨ Features
- Content input via **URL**, **text**, or **document upload**.  
- Automated content rewriting with **tone, structure, accessibility, and SEO guidance**.  
- **Governance report card** with scores.  
- **Side-by-side comparison** of original and improved content.  
- **Download options** for revised content (HTML or Word).

---

## 🚀 Data Sources
- Uses **OpenAI large language models** for advanced content analysis and rewriting.
- Relies on the **Content playbook** document for governance and style rules.
- Follows **accessibility standards** based on the [WCAG 2.1 guidelines](https://www.w3.org/WAI/WCAG21/) and incorporates audits inspired by [Lighthouse Accessibility Scoring](https://developer.chrome.com/docs/lighthouse/accessibility/scoring).
- Implements **SEO best practices** guided by Google's [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide), along with audits for descriptive link text, meta descriptions, and font size legibility using [Lighthouse SEO audits](https://developer.chrome.com/docs/lighthouse/seo/link-text), [meta description checks](https://developer.chrome.com/docs/lighthouse/seo/meta-description), and [font size guidelines](https://developer.chrome.com/docs/lighthouse/seo/font-size).

---

## 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔐 Set Up API Key
```bash
# Create a .env file at the project root with:
# OPENAI_API_KEY = "your_openai_key_here"
```
Or, for Streamlit Cloud deployment, create a .streamlit/secrets.toml file:
```bash
# [api]
# OPENAI_API_KEY = "your_openai_key_here"
```

---

## 🚀 Run the App
```bash
streamlit run src/App.py
```

---

## 🗂️ Project Structure

```bash
cara/
├── src/
│   ├── components/
│   │   ├── layout.py          # UI layout components
│   │   ├── pipeline.py        # Core content transformation logic
│   │   └── style.py           # CSS injection
│   ├── documentation/
│   │   ├── CARA Flowchart.png
│   │   └── flowchart.xml
│   ├── pages/
│   │   ├── About Us.py
│   │   └── Methodology.py
│   ├── resources/
│   │   ├── Word document sample.docx
│   │   └── contentplaybook.docx
│   └── App.py                 # Main Streamlit app
├── requirements.txt           # Dependency list
├── .env                       # (Self setup) Local API key
├── .gitignore                 # (Self setup) 
└── README.md                  # Project documentation
```
