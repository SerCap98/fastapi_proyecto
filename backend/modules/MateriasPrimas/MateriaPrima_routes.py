from fastapi import APIRouter, Body, Depends, Path, status
from databases import Database
from modules.MateriasPrimas.MateriaPrima_schemas import MateriaPrima, MateriaPrimaInDB
from modules.MateriasPrimas.MateriaPrima_services import MateriaPrimaService
from shared.utils.service_result import handle_result
from shared.core.db.db_dependencies import get_database

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=MateriaPrimaInDB,name="MateriaPrima:create-MateriaPrima", status_code=status.HTTP_201_CREATED)
async def create_materia_prima(
    materia_prima: MateriaPrima = Body(..., embed=True),
    db: Database = Depends(get_database)
):
    result = await MateriaPrimaService(db).create_materia_prima(materia_prima)
    return handle_result(result)

@router.get("/{id}",name="MateriaPrima:get-MateriaPrima-by-id", response_model=MateriaPrimaInDB)
async def get_materia_prima_by_id(
    id: str = Path(..., title="The ID of the materia prima to retrieve"),
    db: Database = Depends(get_database)
):
    result = await MateriaPrimaService(db).get_materia_prima_by_id(id)
    return handle_result(result)

# Puedes agregar aquí más rutas para actualizar, eliminar, y listar materias primas.
