from datetime import date, datetime

from pydantic import BaseModel


class SupplierBaseSchema(BaseModel):
    title: str
    inn: str


class SupplierCreateSchema(SupplierBaseSchema):
    address: str
    description: str


class SupplierResponseSchema(SupplierCreateSchema):
    id: int


class SupplierListSchema(SupplierBaseSchema):
    id: int


class SuppliesSchema(BaseModel):
    document_number: str
    document_data: date
    supplier_id: int
    warehouse_id: int
    draft: bool


class SuppliesBaseResponseSchema(SuppliesSchema):
    created: datetime
    updated: datetime
    id: int


class SuppliesWithSuppliersSchema(SuppliesBaseResponseSchema):
    supplier: SupplierListSchema


class SuppliesAddProductSchema(BaseModel):
    product_id: int
    quantity: int
    price: float
