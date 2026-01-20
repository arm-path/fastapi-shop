from pydantic import BaseModel


class ProductCartEditSchema(BaseModel):
    quantity: int

class ProductCartCreateSchema(ProductCartEditSchema):
    product_id: int


class ProductCartResponseSchema(ProductCartCreateSchema):
    cart_id: int
    id: int
