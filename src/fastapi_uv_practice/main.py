from fastapi import FastAPI, HTTPException
from .routers.products import router as product_router
from .routers.llm import router as llm_router

app = FastAPI()

app.include_router(product_router)
app.include_router(llm_router)

@app.get("/")
def home():
    return {"message": "Hello world!"}