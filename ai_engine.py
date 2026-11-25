import os
import warnings
warnings.filterwarnings("ignore")

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    # Try Streamlit Cloud Secrets first, then local .env
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY")

def ask_ai(customer_issue, company_policy, language="English"):
    genai.configure(api_key=get_api_key())
    rules = f"""
    You are the A.I.R.S. Customer Support Assistant.
    Read the Company Policy below and solve the Customer Issue.

    LANGUAGE INSTRUCTION:
    Respond entirely in: {language}.

    STRICT RESOLUTION RULES:
    1. If the Company Policy clearly explains how to solve the issue, provide clear, numbered step-by-step instructions in {language}.
    2. If the Company Policy does NOT contain the answer, or if the customer needs human assistance, reply with ONLY the single word: UNRESOLVED
    3. Do NOT translate the word UNRESOLVED into other languages. Keep it exactly as UNRESOLVED.
    """

    model = genai.GenerativeModel(
        model_name="gemini-3.8-flash",
        system_instruction=rules
    )
    prompt = f"Company Policy:\n{company_policy}\n\nCustomer Issue:\n{customer_issue}"
    response = model.generate_content(prompt)
    return response.text.strip()