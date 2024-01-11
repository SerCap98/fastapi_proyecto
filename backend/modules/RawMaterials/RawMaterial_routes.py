from fastapi import APIRouter, Body, Depends, Path, status
from databases import Database

from modules.users.auths.auth_dependencies import get_current_active_user

from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized
from modules.RawMaterials.RawMaterial_schemas import RawMaterial, RawMaterialInDB
from modules.RawMaterials.RawMaterial_services import RawMaterialService
from shared.utils.service_result import ServiceResult, handle_result
from shared.core.db.db_dependencies import get_database
from typing import List
from modules.users.users.user_schemas import  UserInDB



router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=RawMaterialInDB,name="RawMaterial:create-RawMaterial", status_code=status.HTTP_201_CREATED)
async def create_raw_material(
    raw_material: RawMaterial = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "RawMaterial:create-RawMaterial"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await RawMaterialService(db).create_raw_material(raw_material)
        return handle_result(result)



@router.get("/{code}",name="RawMaterial:get-RawMaterial-by-code", response_model=RawMaterialInDB,status_code=status.HTTP_200_OK)
async def get_raw_material_by_code(
    code: str = Path(..., title="The code of the raw material to retrieve"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "RawMaterial:get-RawMaterial-by-code"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await RawMaterialService(db).get_raw_material_by_code(code)
        return handle_result(result)


@router.get("/all/", name="RawMaterial:get-all-RawMaterials",response_model=List[RawMaterialInDB],status_code=status.HTTP_200_OK)
async def get_all_raw_materials(
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
    ):
    if not is_authorized(current_user, "RawMaterial:get-all-RawMaterials"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await RawMaterialService(db).get_all_raw_materials()
        return handle_result(result)

@router.delete("/{code}", response_model=dict, name="RawMaterial:delete-RawMaterial-by-code",status_code=status.HTTP_200_OK)
async def delete_raw_material_by_code(
    code: str = Path(..., title="The code of the raw material to delete"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "RawMaterial:delete-RawMaterial"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await RawMaterialService(db).delete_raw_material_by_code(code)
        return handle_result(result)

@router.put("/{code}", response_model=RawMaterialInDB, name="RawMaterial:update-RawMaterial-by-code",status_code=status.HTTP_200_OK)
async def update_raw_material_by_code(
    code: str = Path(..., title="The code of the raw material to update"),
    raw_material_update: RawMaterial = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "RawMaterial:update-RawMaterial-by-code"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await RawMaterialService(db).update_raw_material_by_code(code, raw_material_update)
        return handle_result(result)