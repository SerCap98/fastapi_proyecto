from fastapi import APIRouter
from modules.users import users_router
from modules.RawMaterials import raw_materials_router

router = APIRouter()

router.include_router(users_router)
router.include_router(raw_materials_router)
