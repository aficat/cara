import os
import json
import openai

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Basic UI
st.title("🤖 GenAI Chatbot")
user_input = st.text_input("You:", "")

if user_input:
    llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.7)
    response = llm([HumanMessage(content=user_input)])
    st.markdown(f"**Bot:** {response.content}")
