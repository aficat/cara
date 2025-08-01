# 🧠 Ask CARA – Content Authoring & Review Assistant
Designed and developed by Afiqah Rashid

**Ask CARA** is your personal content governance assistant designed to help CPF product owners and content authors confidently create and review high-quality citizen-facing content.

CARA takes in a CPF page draft and enhances it by:

- Recommending the right structure  
- Rewriting with the correct voice, tone, and hierarchy  
- Checking accessibility and SEO compliance  
- Generating a governance report card

Built With
- Python 3.8+
- Streamlit
= OpenAI API

---

## ✨ Key Features

- 📄 **Content Input Options**
  - Paste content manually
  - Provide a CPF.gov.sg hyperlink
  - Upload a `.docx` file

- 🧠 **Smart Analysis**
  - Understands content intent and type
  - Suggests heading hierarchy based on CPF templates

- 🪄 **Optimised Rewriting**
  - Rewrites in CPF tone and voice
  - Improves structure, hierarchy, SEO and accessibility

- 📊 **Governance Report Card**
  - Summarises issues with structure, tone, readability and more

- 🖥️ **Responsive UI**
  - Clean layout based on common UX writing assistants

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-username/ask-cara.git
cd ask-cara
```

## Install Dependencies
pip install -r requirements.txt

## Set Up API Key
# Create a .env file at the project root with:
# OPENAI_API_KEY=your_openai_key_here

# Or, for Streamlit Cloud deployment, create a .streamlit/secrets.toml:
# [api]
# openai_key = "your_openai_key_here"

## Run the App
streamlit run main.py

## Project Structure
cara/
├── components/
│   ├── layout.py          # UI layout components
│   ├── pipeline.py        # Core content transformation logic
│   └── style.py           # CSS injection
├── main.py                # Main Streamlit app
├── requirements.txt       # Dependency list
├── .env                   # (Optional) Local API key
└── README.md              # This file





