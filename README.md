# 🤖 A.I.R.S. – AI-Powered Issue Resolution & Escalation System

**B.Tech 2nd Year Project**  
**Domain:** Generative AI / Agentic AI / Full-Stack Development

## 📌 Project Overview
**A.I.R.S.** is an intelligent multi-company customer support assistant built using **Retrieval-Augmented Generation (RAG)** and **Google Gemini AI**. 
- **Instant Resolution:** Searches official company FAQ knowledge bases using Cosine Similarity vector matching to provide step-by-step troubleshooting.
- **Smart Human Escalation:** Automatically detects complex or unresolvable complaints (`UNRESOLVED`) and triggers a one-click verified human escalation card fetched from an **SQLite** database.
- **Live Analytics:** Tracks total queries, AI-resolved issues, and human escalations in real time.

## 🛠️ Tech Stack
- **Language:** Python
- **AI Engine:** Google Gemini API (`gemini-3.8-flash`)
- **Vector Search (RAG):** Custom Cosine Similarity Vector Store (`vector_store.py`)
- **Database (DBMS):** SQLite3 (`airs_database.db`)
- **Web Scraper:** BeautifulSoup4
- **Frontend UI:** Streamlit