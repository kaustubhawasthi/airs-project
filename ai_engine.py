import os
import warnings

warnings.filterwarnings("ignore")

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


def ask_ai(customer_issue, company_policy, language="English"):
    rules = f"""
    You are the A.I.R.S. Customer Support Assistant.
    Read the Company Policy below and solve the Customer Issue.

    LANGUAGE INSTRUCTION:
    Respond entirely in: {language}.
    (For example, if Hindi is requested, reply in natural Hindi script. If Hinglish is requested, reply in Hindi written with English letters).

    STRICT RESOLUTION RULES:
    1. If the Company Policy clearly explains how to solve the issue, provide clear, numbered step-by-step instructions in {language}.
    2. If the Company Policy does NOT contain the answer, or if the customer needs human assistance (such as a missing refund, driver issue, damaged item, or account lock), reply with ONLY the single word: UNRESOLVED
    3. Do NOT translate the word UNRESOLVED into other languages. Keep it exactly as UNRESOLVED so the code can catch it.
    """

    model = genai.GenerativeModel(
        model_name="gemini-3.8-flash",
        system_instruction=rules
    )
    prompt = f"Company Policy:\n{company_policy}\n\nCustomer Issue:\n{customer_issue}"
    response = model.generate_content(prompt)
    return response.text.strip()


if __name__ == "__main__":
    sample_policy = "To reset your password, go to Settings > Security > Reset Password and enter the OTP."
    print("Testing Hindi:")
    print(ask_ai("How do I reset my password?", sample_policy, language="Hindi"))