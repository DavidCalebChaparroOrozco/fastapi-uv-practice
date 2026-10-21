from fastapi import FastAPI, HTTPException
from .routers.products import router as product_router

app = FastAPI()

app.include_router(product_router)

@app.get("/")
def home():
    return {"message": "Hello world!"}