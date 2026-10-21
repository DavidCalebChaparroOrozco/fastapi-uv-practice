from fastapi import FastAPI
from .schemas import Product

app = FastAPI()

products: dict[int, Product] = {}
next_id: int = 1 

@app.get("/")
def home():
    return {"message": "Hello world!"}

@app.get("/products")
def get_products(limit: int = 10):
    return list(products.values())[:limit]


@app.get("/products/{product_id}")
def get_product(product_id: int):
    return products.get(product_id)


@app.post("/products", status_code=201)
def create_product(product: Product):
    global next_id

    product.id = next_id
    products[next_id] = product
    next_id += 1

    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    return products.pop(product_id, None)