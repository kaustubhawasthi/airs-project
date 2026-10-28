from vector_store import search_knowledge
from ai_engine import ask_ai
from db import get_company_details


def handle_customer_issue(company_name, customer_query, language="English"):
    # Step 1: Search Vector DB for matching rules
    matched_rules = search_knowledge(company_name, customer_query)

    # Step 2: Ask Gemini AI to solve it in the user's chosen language
    ai_response = ask_ai(customer_query, matched_rules, language=language)

    # Step 3: Check if unresolved
    if "UNRESOLVED" in ai_response.upper():
        contacts = get_company_details(company_name)
        return {
            "status": "ESCALATED",
            "message": "Escalating to human support:",
            "contacts": contacts
        }
    else:
        return {
            "status": "RESOLVED",
            "solution": ai_response
        }