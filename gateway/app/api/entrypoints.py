from fastapi import APIRouter

from .products.entrypoints import router as products_router
from .carts.entrypoints import router as carts_router

router = APIRouter()

router.include_router(products_router, tags=['products'], prefix='/products')
router.include_router(carts_router, tags=['carts'], prefix='/carts')
