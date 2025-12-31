from typing import Literal, List

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


class CharacteristicDetailSchema(CharacteristicSchema):
    id: int


class CategoryWithCharacteristicSchema(CategoryItemSchema):
    characteristics: List[CharacteristicDetailSchema]


class CategoryDetailSchema(CategoryItemSchema):
    categories: List[CategoryItemSchema]


class CategoryDetailWithCharacteristicSchema(CategoryDetailSchema):
    characteristics: List[CategoryItemSchema]


class ProductSchema(BaseModel):
    title: str
    category_id: int
    price: float
    discount: int
    description: str | None = None


class ProductCharacteristicSchema(BaseModel):
    characteristic_id: int
    value: str


class ProductCharacteristicSchemaUpdate(BaseModel):
    id: int
    value: str
