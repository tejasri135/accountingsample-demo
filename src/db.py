import sqlite3

def get_connection():
    return sqlite3.connect("gst.db")

def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            base_price REAL,
            tax_rate INTEGER,
            purchase_date TEXT
        )
    """)
    conn.commit()
    conn.close()

create_table()

def add_purchase(product_name, base_price, tax_rate, purchase_date):
    conn = get_connection()
    conn.execute(
        "INSERT INTO purchases (product_name, base_price, tax_rate, purchase_date) VALUES (?, ?, ?, ?)",
        (product_name, base_price, tax_rate, purchase_date)
    )
    conn.commit()
    conn.close()


def get_all_purchases():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM purchases").fetchall()
    conn.close()
    return rows
