from datetime import datetime
from typing import List, TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import DuplicateProductError
from app.order.models import Order, OrderProduct
from app.order.schemas import ProductOrderSchema

if TYPE_CHECKING:
    from app.user.models import User


class OrderService:
    @classmethod
    async def create(cls, session: AsyncSession, user: User, data: List[ProductOrderSchema]):
        try:
            order = Order(user_id=user.id, is_payment=False, is_active=False)
            session.add(order)
            await session.flush()
            await session.refresh(order)
            order_products = []
            product_ids = set()
            for el in data:
                if el.product_id in product_ids:
                    raise DuplicateProductError(f'Duplicate product_id: {el.product_id}')

                product_ids.add(el.product_id)
                order_products.append(
                    OrderProduct(product_id=el.product_id, order_id=order.id, quantity=el.quantity, price=el.price)
                )
            session.add_all(order_products)
            await session.flush()
            order.is_active = True
            order.updated = datetime.utcnow()
            await session.commit()
        except IntegrityError as e:
            print('OrderService.create -> ', e)
            await session.rollback()
            if e.orig.pgcode == '23503':
                raise HTTPException(status_code=400, detail='ID non-existent product')
        except DuplicateProductError as e:
            print('OrderService.create -> ', e)
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            print('OrderService.create -> ', e)
            await session.rollback()
            raise HTTPException(status_code=500, detail='Database error')
