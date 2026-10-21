from fastapi import APIRouter, HTTPException
from ..schemas import Product
from .. import storage

router = APIRouter(
    prefix= "/products",
    tags=["products"],
)


@router.get("/")
def get_products(limit: int = 10):
    return list(storage.products.values())[:limit]


@router.get("/{product_id}")
def get_product(product_id: int):
    product = storage.products.get(product_id)

    if not product:
        raise HTTPException(
            status_code = 404,
            detail = f"Product with id {product_id} not found"
        )

@router.post("/", status_code=201)
def create_product(product: Product):

    product.id = storage.next_id
    storage.products[storage.next_id] = product
    storage.next_id += 1

    return product

@router.delete("/{product_id}")
def delete_product(product_id: int):
    product = storage.products.pop(product_id, None)

    if not product:
        raise HTTPException(
            status_code = 404,
            detail = f"Product with id {product_id} not found"
        )