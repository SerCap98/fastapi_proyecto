from fastapi import APIRouter

from modules.MateriasPrimas.MateriaPrima_routes import router as materia_prima_router

materias_primas_router = APIRouter(
    prefix="/materias-primas",
    tags=["materias-primas"],
    responses={404: {"description": "Not found"}},
)

# Aquí incluyes las rutas específicas de materias primas
materias_primas_router.include_router(materia_prima_router)
