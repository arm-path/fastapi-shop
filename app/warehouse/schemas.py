from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, Field


class SupplierBaseSchema(BaseModel):
    title: str
    inn: int = Annotated[int, Field(max_digits=12)]


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
    draft: bool


class SuppliesBaseResponseSchema(SuppliesSchema):
    created: datetime
    updated: datetime
    id: int

