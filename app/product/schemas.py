from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    title: str = Field(max_length=255)


class CategoryListSchema(CategorySchema):
    id: int


class CategoryItemSchema(CategoryListSchema):
    slug: str
