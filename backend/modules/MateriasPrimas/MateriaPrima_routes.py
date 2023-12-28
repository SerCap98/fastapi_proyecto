from fastapi import APIRouter, Body, Depends, Path, status
from databases import Database
from modules.MateriasPrimas.MateriaPrima_schemas import MateriaPrima, MateriaPrimaInDB
from modules.MateriasPrimas.MateriaPrima_services import MateriaPrimaService
from shared.utils.service_result import handle_result
from shared.core.db.db_dependencies import get_database
from typing import List

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

@router.get("/{codigo}",name="MateriaPrima:get-MateriaPrima-by-code", response_model=MateriaPrimaInDB,status_code=status.HTTP_200_OK)
async def get_materia_prima_by_code(
    codigo: str = Path(..., title="The code of the materia prima to retrieve"),
    db: Database = Depends(get_database)
):
    result = await MateriaPrimaService(db).get_materia_prima_by_code(codigo)
    return handle_result(result)


@router.get("/all/", name="MateriaPrima:get-all-MateriasPrimas",response_model=List[MateriaPrimaInDB],status_code=status.HTTP_200_OK)
async def get_all_materias_primas(db: Database = Depends(get_database)):
    result = await MateriaPrimaService(db).get_all_materias_primas()
    return handle_result(result)

@router.delete("/{codigo}", response_model=dict, name="MateriaPrima:delete-MateriaPrima-by-code",status_code=status.HTTP_200_OK)
async def delete_materia_prima_by_code(
    codigo: str = Path(..., title="The code of the materia prima to delete"),
    db: Database = Depends(get_database)
):
    result = await MateriaPrimaService(db).delete_materia_prima_by_code(codigo)
    return handle_result(result)

@router.put("/{codigo}", response_model=MateriaPrimaInDB, name="MateriaPrima:update-MateriaPrima-by-code",status_code=status.HTTP_200_OK)
async def update_materia_prima_by_code(
    codigo: str = Path(..., title="The code of the materia prima to update"),
    materia_prima_update: MateriaPrima = Body(..., embed=True),
    db: Database = Depends(get_database)
):
    result = await MateriaPrimaService(db).update_materia_prima_by_code(codigo, materia_prima_update)
    return handle_result(result)
