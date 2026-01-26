from typing import List

from pydantic import BaseModel, Field


class ProductCartEditSchema(BaseModel):
    quantity: int = Field(gt=1, )


class ProductCartCreateSchema(ProductCartEditSchema):
    product_id: int


class ProductCartResponseSchema(ProductCartCreateSchema):
    cart_id: int
    id: int

class ProductInCartSchema(BaseModel):
    id: int
    product: str
    quantity: int
    warehouse: int
    price: int
    total: int

class CartResponseSchema(BaseModel):
    cart: int
    items: List[ProductInCartSchema]
    total: int