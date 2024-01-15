from fastapi import APIRouter

from modules.RawMaterialOrder.RawMaterialOrder_routes import router as RawMaterialOrder_router

RawMaterialOrders_router = APIRouter(
    prefix="/RawMaterialOrder",
    tags=["RawMaterialOrder"],
    responses={404: {"description": "Not found"}},
)

# Rutas específicas de productos
RawMaterialOrders_router.include_router(RawMaterialOrder_router)