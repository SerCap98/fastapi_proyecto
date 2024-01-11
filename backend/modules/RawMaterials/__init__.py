
from fastapi import APIRouter

from backend.modules.RawMaterials.RawMaterial_routes import router as raw_material_router

raw_materials_router = APIRouter(
    prefix="/raw-materials",
    tags=["raw-materials"],
    responses={404: {"description": "Not found"}},
)

# Aquí incluyes las rutas específicas de materias primas
raw_materials_router.include_router(raw_material_router)
