from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.product import router as product_router

app = FastAPI(title='SHOP', version='1.0')
add_pagination(app)

app.include_router(product_router)
