
from fastapi import APIRouter

from modules.ManufacturedProduct.ManufacturedProduct_routes import router as manufactured_product_router

manufactured_products_router = APIRouter(
    prefix="/manufactured-products",
    tags=["manufactured-products"],
    responses={404: {"description": "Not found"}},
)

# Rutas específicas de productos manufacturados
manufactured_products_router.include_router(manufactured_product_router)
