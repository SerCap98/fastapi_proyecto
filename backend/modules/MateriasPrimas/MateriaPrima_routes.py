from fastapi import APIRouter, Body, Depends, Path, status
from databases import Database

from modules.users.auths.auth_dependencies import get_current_active_user

from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized
from modules.MateriasPrimas.MateriaPrima_schemas import MateriaPrima, MateriaPrimaInDB
from modules.MateriasPrimas.MateriaPrima_services import MateriaPrimaService
from shared.utils.service_result import ServiceResult, handle_result
from shared.core.db.db_dependencies import get_database
from typing import List
from modules.users.users.user_schemas import  UserInDB



router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=MateriaPrimaInDB,name="MateriaPrima:create-MateriaPrima", status_code=status.HTTP_201_CREATED)
async def create_materia_prima(
    materia_prima: MateriaPrima = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "MateriaPrima:create-MateriaPrima"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await MateriaPrimaService(db).create_materia_prima(materia_prima)
        return handle_result(result)



@router.get("/{codigo}",name="MateriaPrima:get-MateriaPrima-by-code", response_model=MateriaPrimaInDB,status_code=status.HTTP_200_OK)
async def get_materia_prima_by_code(
    codigo: str = Path(..., title="The code of the materia prima to retrieve"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "MateriaPrima:get-MateriaPrima-by-code"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await MateriaPrimaService(db).get_materia_prima_by_code(codigo)
        return handle_result(result)


@router.get("/all/", name="MateriaPrima:get-all-MateriasPrimas",response_model=List[MateriaPrimaInDB],status_code=status.HTTP_200_OK)
async def get_all_materias_primas(
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
    ):
    if not is_authorized(current_user, "MateriaPrima:get-all-MateriasPrimas"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await MateriaPrimaService(db).get_all_materias_primas()
        return handle_result(result)

@router.delete("/{codigo}", response_model=dict, name="MateriaPrima:delete-MateriaPrima-by-code",status_code=status.HTTP_200_OK)
async def delete_materia_prima_by_code(
    codigo: str = Path(..., title="The code of the materia prima to delete"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "MateriaPrima:delete-MateriaPrima"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await MateriaPrimaService(db).delete_materia_prima_by_code(codigo)
        return handle_result(result)

@router.put("/{codigo}", response_model=MateriaPrimaInDB, name="MateriaPrima:update-MateriaPrima-by-code",status_code=status.HTTP_200_OK)
async def update_materia_prima_by_code(
    codigo: str = Path(..., title="The code of the materia prima to update"),
    materia_prima_update: MateriaPrima = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "MateriaPrima:update-MateriaPrima-by-code"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await MateriaPrimaService(db).update_materia_prima_by_code(codigo, materia_prima_update)
        return handle_result(result)
