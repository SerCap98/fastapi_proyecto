
from fastapi import APIRouter

from modules.Warehouse.Warehouse_routes import router as Warehouse_router

Warehouses_router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse"],
    responses={404: {"description": "Not found"}},
)

# rutas específicas de Warehouse
Warehouses_router.include_router(Warehouse_router)
