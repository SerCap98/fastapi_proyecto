
from fastapi import APIRouter

from modules.Product.Product_routes import router as product_router

products_router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

# Rutas específicas de productos
products_router.include_router(product_router)
