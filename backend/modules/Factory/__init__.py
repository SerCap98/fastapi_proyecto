from fastapi import APIRouter

from modules.Factory.Factory_routes import router as factory_router

factory_router = APIRouter(
    prefix="/factory",
    tags=["factory"],
    responses={404: {"description": "Not found"}},
)

# Rutas específicas de la fábrica
factory_router.include_router(factory_router)
