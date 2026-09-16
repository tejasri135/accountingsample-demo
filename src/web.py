from fastapi import FastAPI, Form,Request
from src.product import Product
from fastapi.responses import HTMLResponse
from src.rates import gst_rates
from fastapi.responses import RedirectResponse
from datetime import date
from src.db import get_all_purchases, add_purchase, get_monthly_reports, get_yearly_reports, check_login, create_user,get_user_id
from starlette.middleware.sessions import SessionMiddleware

today = date.today()
month_label = today.strftime("%B %Y")   # e.g. "September 2026"
year_label = today.strftime("%Y")        # e.g. "2026"
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="change-this-to-a-random-string")

@app.get("/register", response_class=HTMLResponse)
def register():
    return """
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; }
        .box { width: 300px; margin: 100px auto; padding: 30px; background: white;
               border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h2 { color: #1a3a6b; text-align: center; }
        input { width: 100%; padding: 10px; margin: 8px 0; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #1a3a6b; color: white;
                 border: none; border-radius: 4px; cursor: pointer; }
    </style>
    <div class="box">
        <h2>Sign Up</h2>
        <form action="/do-register" method="post">
            <input name="username" placeholder="Username">
            <input name="password" type="password" placeholder="Password">
            <button type="submit">Register</button>
        </form>
    </div>
    """
    
    
@app.get("/login", response_class=HTMLResponse)
def login(registered: str = ""):
    message = ""
    if registered:
        message = "<p style='color:green;text-align:center;'>New user added! Please login with your credentials.</p>"
    return f"""
    <style>
        body {{ font-family: Arial, sans-serif; background: #f0f2f5; }}
        .box {{ width: 300px; margin: 100px auto; padding: 30px; background: white;
               border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h2 {{ color: #1a3a6b; text-align: center; }}
        input {{ width: 100%; padding: 10px; margin: 8px 0; box-sizing: border-box; }}
        button {{ width: 100%; padding: 10px; background: #1a3a6b; color: white;
                 border: none; border-radius: 4px; cursor: pointer; }}
    </style>
    <div class="box">
        <h2>Login</h2>
        {message}
        <form action="/do-login" method="post">
            <input name="username" placeholder="Username">
            <input name="password" type="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>
    </div>
    """

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
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; }
        .box { max-width: 420px; margin: 40px auto; padding: 30px; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h2 { color: #1a3a6b; }
        input, select { width: 100%; padding: 8px; margin: 4px 0; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #1a3a6b; color: white; border: none; border-radius: 4px; }
    </style>
    <div class="box">
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
def report(request: Request):
    user = request.session.get("user")
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    user_id = get_user_id(user) 
    rows = get_all_purchases(user_id)
    
    html = """
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; color: #1a1a1a; }
        .invoice-title { font-size: 40px; font-weight: bold; color: #1a3a6b; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th { background: #1a3a6b; color: white; padding: 10px; text-align: left; }
        td { padding: 8px 12px; border: 1px solid #ccc; }
        .totals { margin-top: 20px; width: 350px; margin-left: auto; }
    </style>
    <div class="invoice-title">INVOICE</div>
    """
    html += f'<p>Welcome {user} | <a href="/logout">Logout</a></p>'
    html += '<a href="/form">+ Add another purchase</a>'
    html += "<table>"
    html += "<tr><th>SL No</th><th>Product</th><th>Base</th><th>Rate</th><th>Date</th><th>CGST</th><th>SGST</th><th>IGST</th><th>Total</th></tr>" 
    grand_total = 0
    for row in rows:
        grand_total += row[8]
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td><td>{row[7]}</td><td>{row[8]}</td></tr>"
    html += f"<tr><th colspan='8'>Grand Total</th><th>{grand_total}</th></tr>"
    html += "</table>"
    
    m = get_monthly_reports(user_id)
    html += f"<h3>Current Month - {month_label}</h3>"
    html += "<table>"
    html += f"<tr><td>Taxable Amount</td><td>{m[0]}</td></tr>"
    html += f"<tr><td>CGST</td><td>{m[1]}</td></tr>"
    html += f"<tr><td>SGST</td><td>{m[2]}</td></tr>"
    html += f"<tr><td>IGST</td><td>{m[3]}</td></tr>"
    
    html += f"<tr><td>Total Tax</td><td>{m[1] + m[2] + m[3]}</td></tr>"

    html += f"<tr><td>Total Payable</td><td>{m[0] + m[1] + m[2] + m[3]}</td></tr>"
    html += "</table>"

    y = get_yearly_reports(user_id)
    html += f"<h3>Current Year - {year_label}</h3>"
    html += "<table>"
    html += f"<tr><td>Taxable Amount</td><td>{y[0]}</td></tr>"
    html += f"<tr><td>CGST</td><td>{y[1]}</td></tr>"
    html += f"<tr><td>SGST</td><td>{y[2]}</td></tr>"
    html += f"<tr><td>IGST</td><td>{y[3]}</td></tr>"
    
    html += f"<tr><td>Total Tax</td><td>{y[1] + y[2] + y[3]}</td></tr>"
    html += f"<tr><td>Total Payable</td><td>{y[0] + y[1] + y[2] + y[3]}</td></tr>"

    html += "</table>"
    return html

@app.get("/add")
def add(request: Request, product_name: str, base: int, purchase_type: str, purchase_date: str, interstate: bool = False):
    user = request.session.get("user")
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    user_id = get_user_id(user)
    rate = gst_rates.get(purchase_type, 18)
    p = Product(product_name, base, rate, interstate)
    result = p.calculate_gst()
    add_purchase(product_name, base, rate, purchase_date,
                 result['cgst'], result['sgst'], result['igst'], result['total_product_price'], user_id)
    return RedirectResponse(url="/report", status_code=303)

@app.post("/do-login")
def do_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if check_login(username, password):
        request.session["user"] = username      # ← the wristband
        return RedirectResponse(url="/report", status_code=303)
    else:
        return HTMLResponse("<h3>Wrong username or password. <a href='/login'>Try again</a></h3>")
    
    
@app.post("/do-register")
def do_register(username: str = Form(...), password: str = Form(...)):
    try:
        create_user(username, password)
        return RedirectResponse(url="/login?registered=1", status_code=303)
    except Exception as e:
        return HTMLResponse(f"<h3>Error: {e}</h3>")    
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)   