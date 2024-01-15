
from fastapi import APIRouter

from modules.OrderProduct.OrderProduct_routes import router as OrderProduct_router

OrderProducts_router = APIRouter(
    prefix="/OrderProduct",
    tags=["OrderProduct"],
    responses={404: {"description": "Not found"}},
)

# Rutas específicas de ordenes de producto
OrderProducts_router.include_router(OrderProduct_router)
