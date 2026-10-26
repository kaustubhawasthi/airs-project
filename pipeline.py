from vector_store import search_knowledge
from ai_engine import ask_ai
from db import get_company_details


def handle_customer_issue(company_name, customer_query):
    # Step 1: Search our Vector Database for this company's matching FAQ rules
    matched_rules = search_knowledge(company_name, customer_query)

    # Step 2: Ask Gemini AI to solve the issue using those rules
    ai_response = ask_ai(customer_query, matched_rules)

    # Step 3: Check if the AI solved it or if it needs human escalation
    if "UNRESOLVED" in ai_response.upper():
        # Fetch phone number, email, and link from our SQLite database
        contacts = get_company_details(company_name)
        return {
            "status": "ESCALATED",
            "message": "Our AI could not resolve this automatically. Escalating to human support:",
            "contacts": contacts
        }
    else:
        return {
            "status": "RESOLVED",
            "solution": ai_response
        }


# Let's test the complete connected system!
if __name__ == "__main__":
    print("=== CASE 1: Swiggy Order Cancellation (Solvable) ===")
    test1 = handle_customer_issue("Swiggy", "I just placed an order 20 seconds ago, can I cancel it for a full refund?")
    print("Status:", test1["status"])
    print("Solution:\n", test1.get("solution"))

    print("\n" + "=" * 50 + "\n")

    print("=== CASE 2: Flipkart Missing Item (Needs Human Escalation) ===")
    test2 = handle_customer_issue("Flipkart",
                                  "I ordered a laptop but the box had a brick inside! Give me my money back immediately!")
    print("Status:", test2["status"])
    print(test2.get("message"))
    print("Escalation Contacts:", test2.get("contacts"))