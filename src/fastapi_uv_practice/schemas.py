from pydantic import BaseModel, Field
# from typing import Optional

class Product(BaseModel):
    id: int | None = None
    name: str = Field(min_length=3)
    description: str | None = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)