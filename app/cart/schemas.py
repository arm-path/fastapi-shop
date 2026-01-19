from pydantic import BaseModel


class ProductCartCreateSchema(BaseModel):
    product_id: int
    quantity: int


class ProductCartResponseSchema(ProductCartCreateSchema):
    cart_id: int
    id: int
