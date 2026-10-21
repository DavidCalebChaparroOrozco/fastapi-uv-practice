from .schemas import Product

products: dict[int, Product] = {}
next_id: int = 1 