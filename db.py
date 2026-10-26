import sqlite3
from datetime import datetime

# 1. Setup both tables: 'escalations' and 'query_logs'
def setup_database():
    connection = sqlite3.connect("airs_database.db")
    cursor = connection.cursor()

    # Table 1: Company Escalation Contacts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS escalations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT UNIQUE NOT NULL,
        support_phone TEXT,
        support_email TEXT,
        help_url TEXT
    )
    """)

    # Table 2: Live Customer Query Logs (for Analytics)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS query_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        customer_query TEXT,
        status TEXT,
        timestamp TEXT
    )
    """)

    companies = [
        ("Amazon", "1800-3000-9009", "cs-reply@amazon.in", "https://www.amazon.in/help"),
        ("Swiggy", "080-6746-6729", "support@swiggy.in", "https://www.swiggy.com/contact-us"),
        ("Flipkart", "1800-208-9898", "support@flipkart.com", "https://www.flipkart.com/helpcentre")
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO escalations (company_name, support_phone, support_email, help_url)
    VALUES (?, ?, ?, ?)
    """, companies)

    connection.commit()
    connection.close()


# 2. Fetch company helpline details
def get_company_details(name_of_company):
    connection = sqlite3.connect("airs_database.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT company_name, support_phone, support_email, help_url 
    FROM escalations 
    WHERE LOWER(company_name) = LOWER(?)
    """, (name_of_company,))

    row = cursor.fetchone()
    connection.close()

    if row:
        return {
            "company": row[0],
            "phone": row[1],
            "email": row[2],
            "link": row[3]
        }
    return None


# 3. Save every customer query into the database
def log_query(company_name, customer_query, status):
    connection = sqlite3.connect("airs_database.db")
    cursor = connection.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO query_logs (company_name, customer_query, status, timestamp)
    VALUES (?, ?, ?, ?)
    """, (company_name, customer_query, status, now))

    connection.commit()
    connection.close()


# 4. Count total, resolved, and escalated queries for the sidebar dashboard
def get_stats():
    connection = sqlite3.connect("airs_database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM query_logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM query_logs WHERE status = 'RESOLVED'")
    resolved = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM query_logs WHERE status = 'ESCALATED'")
    escalated = cursor.fetchone()[0]

    connection.close()
    return {"total": total, "resolved": resolved, "escalated": escalated}