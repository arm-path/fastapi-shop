from datetime import datetime
from typing import Literal, TYPE_CHECKING

from sqlalchemy import String, Boolean, text, event
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database import Base
from app.cart.models import Cart

if TYPE_CHECKING:
    from app.cart.models import Cart

USER_ROLE_TYPE = Literal['installer', 'manager', 'storekeeper', 'client']
USER_ROLE: list[str] = ['installer', 'manager', 'storekeeper', 'client']


class User(Base):
    first_name: Mapped[str] = mapped_column(String(61), nullable=False)
    last_name: Mapped[str] = mapped_column(String(61), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    role: Mapped[USER_ROLE_TYPE] = mapped_column(ENUM(*USER_ROLE, name='enum_user_role'), default='client')
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    cart: Mapped[Cart] = relationship(back_populates='user')


@event.listens_for(User, 'after_insert')
def create_cart_user(mapper, connection, target):
    connection.execute(Cart.__table__.insert().values(user_id=target.id, ))
