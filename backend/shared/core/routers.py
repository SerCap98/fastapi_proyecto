from fastapi import APIRouter
from modules.users import users_router
from modules.RawMaterials import raw_materials_router
from modules.Factory import factories_router
from modules.Product import products_router
from modules.ManufacturedProduct import manufactured_products_router
from modules.FactoryRawMaterialInventory import FactoryRawMaterialsInventory_router


router = APIRouter()

router.include_router(users_router)
router.include_router(raw_materials_router)
router.include_router(factories_router)
router.include_router(products_router)
router.include_router(manufactured_products_router)
router.include_router(FactoryRawMaterialsInventory_router)
