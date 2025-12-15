from typing import Literal

from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    title: str = Field(max_length=255)
    parent_id: int | None = None


class CategoryListSchema(CategorySchema):
    id: int


class CategoryItemSchema(CategoryListSchema):
    slug: str


class CharacteristicSchema(BaseModel):
    title: str
    unit: str | None = None
    type: Literal['integer', 'float', 'string', 'boolean'] = 'string'
