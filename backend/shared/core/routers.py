from fastapi import APIRouter
from modules.users import users_router
from modules.RawMaterials import raw_materials_router
from modules.Factory import factories_router
from modules.Product import products_router
from modules.ManufacturedProduct import manufactured_products_router
from modules.FactoryRawMaterialInventory import FactoryRawMaterialsInventory_router
from modules.Alert import alerts_router
from modules.Warehouse import Warehouses_router
from modules.Formula import Formulas_router
from modules.WarehouseProductInventory import WarehouseProductInventory_routers
from modules.RawMaterialOrder import RawMaterialOrders_router
from modules.OrderProduct import OrderProducts_router
from modules.Backlog import Backlogs_router

router = APIRouter()

router.include_router(users_router)
router.include_router(raw_materials_router)
router.include_router(factories_router)
router.include_router(products_router)
router.include_router(OrderProducts_router)
router.include_router(manufactured_products_router)
router.include_router(FactoryRawMaterialsInventory_router)
router.include_router(alerts_router)
router.include_router(Warehouses_router)
router.include_router(Formulas_router)
router.include_router(WarehouseProductInventory_routers)
router.include_router(RawMaterialOrders_router)
router.include_router(Backlogs_router)
