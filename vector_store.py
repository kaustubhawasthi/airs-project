import os
import re
import json
import math
from collections import Counter

VECTOR_DB_FILE = "vector_db.json"


# 1. Helper: Turn any sentence into a clean list of words
def get_words(text):
    words = re.findall(r'\w+', text.lower())
    # Ignore tiny common words that don't add meaning
    stop_words = {"the", "a", "an", "to", "in", "on", "of", "and", "or", "is", "are", "for", "your", "you"}
    return [w for w in words if w not in stop_words]


# 2. Helper: Calculate "Cosine Similarity" (how closely two sentences match from 0.0 to 1.0)
def cosine_similarity(query_words, doc_words):
    counter1 = Counter(query_words)
    counter2 = Counter(doc_words)

    # Find words that appear in both the customer's question and the FAQ rule
    common_words = set(counter1.keys()) & set(counter2.keys())
    dot_product = sum(counter1[w] * counter2[w] for w in common_words)

    mag1 = math.sqrt(sum(val ** 2 for val in counter1.values()))
    mag2 = math.sqrt(sum(val ** 2 for val in counter2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product / (mag1 * mag2)


# 3. Build the Vector Database from the 'data/' folder
def build_vector_db():
    db_records = []
    data_folder = "data"

    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            company = filename.replace(".txt", "").lower()
            file_path = os.path.join(data_folder, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                paragraphs = [p.strip() for p in f.read().split("\n\n") if p.strip()]

            for paragraph in paragraphs:
                db_records.append({
                    "company": company,
                    "text": paragraph,
                    "vector_tokens": get_words(paragraph)
                })

    with open(VECTOR_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_records, f, indent=2)

    print(f"Indexed {len(db_records)} FAQ rules into {VECTOR_DB_FILE}!")


# 4. Search the Vector Database for the most relevant company rules
def search_knowledge(company_name, customer_query):
    if not os.path.exists(VECTOR_DB_FILE):
        build_vector_db()

    with open(VECTOR_DB_FILE, "r", encoding="utf-8") as f:
        db_records = json.load(f)

    query_tokens = get_words(customer_query)
    company_name = company_name.lower()

    scored_results = []
    for record in db_records:
        if record["company"] == company_name:
            score = cosine_similarity(query_tokens, record["vector_tokens"])
            scored_results.append((score, record["text"]))

    # Sort from highest match score to lowest
    scored_results.sort(key=lambda x: x[0], reverse=True)

    # Return the top 2 matching rules (or all rules for that company if keywords are phrased differently)
    top_matches = [text for score, text in scored_results[:2] if score > 0]
    if not top_matches:
        # Fallback: pass the company's rules so the AI can check meanings/synonyms
        top_matches = [r["text"] for r in db_records if r["company"] == company_name]

    return "\n\n".join(top_matches)


# 5. Test the Vector Search!
if __name__ == "__main__":
    build_vector_db()

    print("\n--- Testing Vector Search for Amazon ---")
    matched_rule = search_knowledge("Amazon", "How many days does a refund take to reach my bank?")
    print("Best Matched Rule Found:\n", matched_rule)