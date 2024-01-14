from fastapi import APIRouter

from modules.Formula.Formula_routes import router as Formula_router

Formulas_router = APIRouter(
    prefix="/formula",
    tags=["formula"],
    responses={404: {"description": "Not found"}},
)

# Rutas específicas de productos
Formulas_router.include_router(Formula_router)