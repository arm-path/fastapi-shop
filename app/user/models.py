from datetime import datetime
from typing import Literal

from sqlalchemy import String, Boolean, text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.settings.database import Base

role = Literal['installer', 'manager', 'storekeeper', 'client']


class User(Base):
    first_name: Mapped[str] = mapped_column(String(61), nullable=False)
    last_name: Mapped[str] = mapped_column(String(61), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    role: Mapped[role] = mapped_column(
        ENUM('installer', 'manager', 'storekeeper', 'client', name='enum_role'), default='client'
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

