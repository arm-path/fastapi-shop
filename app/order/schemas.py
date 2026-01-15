from pydantic import BaseModel


class ProductOrderSchema(BaseModel):
    product_id: int
    quantity: int
    price: float
