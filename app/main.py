from fastapi import FastAPI

from app.product import router as product_router

app = FastAPI(title='SHOP', version='1.0')

app.include_router(product_router)