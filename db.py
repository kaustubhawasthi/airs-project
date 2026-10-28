import sqlite3
from datetime import datetime

def setup_database():
    connection = sqlite3.connect("airs_database.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS escalations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT UNIQUE NOT NULL,
        support_phone TEXT,
        support_email TEXT,
        help_url TEXT
    )
    """)

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
        ("Flipkart", "1800-208-9898", "support@flipkart.com", "https://www.flipkart.com/helpcentre"),
        ("Swiggy", "080-6746-6729", "support@swiggy.in", "https://www.swiggy.com/contact-us"),
        ("Zomato", "011-3520-0000", "order@zomato.com", "https://www.zomato.com/contact"),
        ("Uber", "1800-103-6950", "support@uber.com", "https://help.uber.com"),
        ("Ola", "080-6735-0900", "support@olacabs.com", "https://help.olacabs.com"),
        ("Paytm", "0120-4456-456", "care@paytm.com", "https://paytm.com/care"),
        ("PhonePe", "080-6872-7374", "grievances@phonepe.com", "https://www.phonepe.com/contact-us"),
        ("Netflix", "000-800-919-1694", "support@netflix.com", "https://help.netflix.com"),
        ("Jio", "198 / 1800-889-9999", "care@jio.com", "https://www.jio.com/help")
    ]

    cursor.executemany("""
    INSERT OR REPLACE INTO escalations (company_name, support_phone, support_email, help_url)
    VALUES (?, ?, ?, ?)
    """, companies)

    connection.commit()
    connection.close()


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


def get_recent_logs(limit=10):
    connection = sqlite3.connect("airs_database.db")
    cursor = connection.cursor()
    cursor.execute("""
    SELECT timestamp, company_name, customer_query, status
    FROM query_logs
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    connection.close()
    return rows


if __name__ == "__main__":
    setup_database()
    print("Database updated with all 10 companies successfully!")