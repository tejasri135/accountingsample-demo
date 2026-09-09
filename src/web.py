from fastapi import FastAPI
from src.product import Product
from fastapi.responses import HTMLResponse

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
    <form action="/calc" method="get">
        Base price: <input name="base" type="number"><br>
        Rate: <input name="rate" type="number"><br>
        Interstate: <input name="interstate" value="false"><br>
        <button type="submit">Calculate</button>
    </form>
    """