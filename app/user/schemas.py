from typing import Self, Literal

from pydantic import BaseModel, field_validator, EmailStr, model_validator

from app.validators import password_validator
from app.user.models import role


class RegistrationSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    password_repeat: str

    @field_validator('password')
    @classmethod
    def check_password_validate(cls, value: str):
        if not password_validator(value):
            raise ValueError('Password complexity violation.')
        return value

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match.')
        return self


class AuthSchema(BaseModel):
    email: EmailStr
    password: str

class UserBaseSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str

class CurrentUserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: role