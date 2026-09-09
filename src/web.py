from fastapi import FastAPI
from src.product import Product
from fastapi.responses import HTMLResponse
from src.db import get_all_purchases,add_purchase,get_monthly_reports, get_yearly_reports
from src.rates import gst_rates
from fastapi.responses import RedirectResponse
from datetime import date

today = date.today()
month_label = today.strftime("%B %Y")   # e.g. "September 2026"
year_label = today.strftime("%Y")        # e.g. "2026"
app = FastAPI()


@app.get("/")
def home():
    return {"message": "GST app is alive"}


@app.get("/calc")
def calc(base: int, rate: int, interstate: bool = False):
    p = Product("item", base, rate, interstate)
    return p.calculate_gst()



@app.get("/form", response_class=HTMLResponse)
def form():
    return """
    <h2>GST Calculator</h2>
<form action="/add" method="get">
    Product: <input name="product_name"><br><br>

    Base price: <input name="base" type="number"><br><br>

    Category:
    <select name="purchase_type">
        <option value="" disabled selected>-- Select category --</option>
        <option value="essentials">Essentials (5%)</option>
        <option value="standard">Standard (12%)</option>
        <option value="electronics">Electronics (18%)</option>
        <option value="luxury">Luxury (28%)</option>
        <option value="misc">Misc (18%)</option>
    </select><br><br>

    Date: <input name="purchase_date" type="date"><br><br>

    Interstate:
    <select name="interstate">
        <option value="false">No (same state)</option>
        <option value="true">Yes (different state)</option>
    </select><br><br>

    <button type="submit">Add Purchase</button>
</form>
    """
    

@app.get("/report", response_class=HTMLResponse)
def report():
    rows = get_all_purchases()
    html = "<h2>Purchases</h2>"
    html += '<a href="/form">+ Add another purchase</a>'
    html += "<table border='1'>"
    html += "<tr><th>ID</th><th>Product</th><th>Base</th><th>Rate</th><th>Date</th><th>CGST</th><th>SGST</th><th>IGST</th><th>Total</th></tr>"
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td><td>{row[8]}</td></tr>"
    html += "</table>"
    
    m = get_monthly_reports()
    html += f"<h3>Current Month - {month_label}</h3>"
    html += "<table border='1'>"
    html += f"<tr><td>Taxable Amount</td><td>{m[0]}</td></tr>"
    html += f"<tr><td>CGST</td><td>{m[1]}</td></tr>"
    html += f"<tr><td>SGST</td><td>{m[2]}</td></tr>"
    html += f"<tr><td>IGST</td><td>{m[3]}</td></tr>"
    html += "</table>"

    y = get_yearly_reports()
    html += f"<h3>Current Year - {year_label}</h3>"
    html += "<table border='1'>"
    html += f"<tr><td>Taxable Amount</td><td>{y[0]}</td></tr>"
    html += f"<tr><td>CGST</td><td>{y[1]}</td></tr>"
    html += f"<tr><td>SGST</td><td>{y[2]}</td></tr>"
    html += f"<tr><td>IGST</td><td>{y[3]}</td></tr>"
    html += "</table>"
    return html

@app.get("/add")
def add(product_name: str, base: int, purchase_type: str, purchase_date: str, interstate: bool = False):
    rate = gst_rates.get(purchase_type, 18)      # ← the lookup, same as CLI
    p = Product(product_name, base, rate, interstate)
    result = p.calculate_gst()
    add_purchase(product_name, base, rate, purchase_date,
                 result['cgst'], result['sgst'], result['igst'], result['total_product_price'])
    ##return {"saved": product_name, "rate_used": rate, "tax": result}
    return RedirectResponse(url="/report", status_code=303)

