from fastapi import APIRouter

from .products.entrypoints import router as products_router

router = APIRouter()

router.include_router(products_router, tags=['products'], prefix='/products')
