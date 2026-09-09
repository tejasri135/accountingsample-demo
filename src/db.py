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
            purchase_date TEXT,
            cgst REAL,
            sgst REAL,
            igst REAL,
            total REAL
        )
    """)
    conn.commit()
    conn.close()

create_table()

def add_purchase(product_name, base_price, tax_rate, purchase_date,cgst,sgst,igst,total):
    conn = get_connection()
    conn.execute(
        "INSERT INTO purchases (product_name, base_price, tax_rate, purchase_date,cgst,sgst,igst,total) VALUES (?, ?, ?, ?,?,?,?,?)",
        (product_name, base_price, tax_rate, purchase_date,cgst,sgst,igst,total)
    )
    conn.commit()
    conn.close()


def get_all_purchases():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM purchases").fetchall()
    conn.close()
    return rows


def get_monthly_reports():
    conn = get_connection()
    row=conn.execute("""select sum(base_price)as taxable,sum(cgst) as cgst,sum(sgst) as sgst,sum(igst) as igst from purchases
                    WHERE strftime('%m', purchase_date) = strftime('%m', 'now')
                    AND strftime('%Y', purchase_date) = strftime('%Y', 'now')                 """
    ).fetchone()
    conn.close()
    return row



def get_yearly_reports():
    conn = get_connection()
    row=conn.execute("""select sum(base_price)as taxable,sum(cgst) as cgst,sum(sgst) as sgst,sum(igst) as igst from purchases
                    WHERE  strftime('%Y', purchase_date) = strftime('%Y', 'now')                 """
    ).fetchone()
    conn.close()
    return row
