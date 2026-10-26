import os
import warnings
warnings.filterwarnings("ignore")

import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the secret key from your .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Connect to Google Gemini
genai.configure(api_key=api_key)

# 3. Give the AI its strict rules
RULES = """
You are the A.I.R.S. Customer Support Assistant.
Read the Company Policy below and try to solve the Customer Issue.

STRICT RULES:
1. If the Company Policy clearly explains how to fix the issue, reply with simple, numbered step-by-step instructions.
2. If the Company Policy does NOT contain the answer, or if the customer needs a human agent (like a missing refund or stolen item), reply with ONLY the single word: UNRESOLVED
"""

def ask_ai(customer_issue, company_policy):
    model = genai.GenerativeModel(
        model_name="gemini-3.8-flash",
        system_instruction=RULES
    )
    prompt = f"Company Policy:\n{company_policy}\n\nCustomer Issue:\n{customer_issue}"
    response = model.generate_content(prompt)
    return response.text.strip()


# 4. Let's test our AI with two examples!
if __name__ == "__main__":
    sample_policy = """
    To reset your password, go to Settings > Security > Reset Password. You will receive an OTP on your registered mobile number.
    Items can be returned within 7 days of delivery if the original tag is attached.
    """

    print("--- TEST 1: A question the AI CAN solve ---")
    answer1 = ask_ai("I forgot my password, how do I change it?", sample_policy)
    print(answer1)

    print("\n--- TEST 2: A question the AI CANNOT solve ---")
    answer2 = ask_ai("The delivery boy stole my parcel and ran away!", sample_policy)
    print(answer2)