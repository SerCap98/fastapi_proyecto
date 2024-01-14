from fastapi import APIRouter

from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_routes import router as FactoryRawMaterialInventory_router

FactoryRawMaterialsInventory_router = APIRouter(
    prefix="/FactRawMatInv",
    tags=["factory-material-inventory"],
    responses={404: {"description": "Not found"}},
)

# Rutas específicas de productos
FactoryRawMaterialsInventory_router.include_router(FactoryRawMaterialInventory_router)