import sqlite3
import bcrypt

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
            purchase_date TEXT,
            cgst REAL,
            sgst REAL,
            igst REAL,
            total REAL,
            user_id text
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    """)
    conn.commit()
    
    conn.close()

create_table()

def add_purchase(product_name, base_price, tax_rate, purchase_date,cgst,sgst,igst,total,user_id):
    conn = get_connection()
    conn.execute(
        "INSERT INTO purchases (product_name, base_price, tax_rate, purchase_date,cgst,sgst,igst,total,user_id) VALUES (?, ?, ?, ?,?,?,?,?,?)",
        (product_name, base_price, tax_rate, purchase_date,cgst,sgst,igst,total,user_id)
    )
    conn.commit()
    conn.close()


def get_all_purchases(user_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM purchases WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return rows


def get_monthly_reports(user_id):
    conn = get_connection()
    row = conn.execute("""
        SELECT COALESCE(sum(base_price),0) as taxable,COALESCE(sum(cgst),0) as cgst,COALESCE(sum(sgst),0) as sgst,COALESCE(sum(igst),0) as igst
        FROM purchases
        WHERE strftime('%m', purchase_date) = strftime('%m', 'now')
        AND strftime('%Y', purchase_date) = strftime('%Y', 'now')
        AND user_id = ?
    """, (user_id,)).fetchone()
    conn.close()
    return row


def get_yearly_reports(user_id):
    conn = get_connection()
    row = conn.execute("""
        SELECT COALESCE(sum(base_price),0) as taxable,COALESCE(sum(cgst),0) as cgst,COALESCE(sum(sgst),0) as sgst,COALESCE(sum(igst),0) as igst
        FROM purchases
        WHERE strftime('%Y', purchase_date) = strftime('%Y', 'now')
        AND user_id = ?
    """, (user_id,)).fetchone()
    conn.close()
    return row

def create_user(username, password):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    conn.commit()
    conn.close()
def check_login(username, password):
    conn = get_connection()
    row = conn.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()
    if row is None:
        return False
    stored_hash = row[0]
    return bcrypt.checkpw(password.encode(), stored_hash)


def get_user_id(username):
    conn = get_connection()
    row = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row[0] if row else None