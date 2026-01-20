from pydantic import BaseModel, Field


class ProductCartEditSchema(BaseModel):
    quantity: int = Field(gt=1, )


class ProductCartCreateSchema(ProductCartEditSchema):
    product_id: int


class ProductCartResponseSchema(ProductCartCreateSchema):
    cart_id: int
    id: int
