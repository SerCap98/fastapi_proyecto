
from fastapi import APIRouter

from modules.WarehouseProductInventory.WarehouseProductInventory_routes import router as WarehouseProductInventory_routes_router

WarehouseProductInventory_routers = APIRouter(
    prefix="/warehouse-product-inventory",
    tags=["warehouse-product-inventory"],
    responses={404: {"description": "Not found"}},
)

# rutas específicas de Warehouse
WarehouseProductInventory_routers.include_router(WarehouseProductInventory_routes_router)
