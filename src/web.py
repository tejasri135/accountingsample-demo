from fastapi import FastAPI
from src.product import Product
app = FastAPI()

@app.get("/")
def home():
    return {"message": "GST app is alive"}


@app.get("/calc")
def calc(base: int, rate: int, interstate: bool = False):
    p = Product("item", base, rate, interstate)
    return p.calculate_gst()