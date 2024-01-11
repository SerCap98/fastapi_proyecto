from fastapi import APIRouter, Body, Depends, Path, status
from databases import Database

from modules.users.auths.auth_dependencies import get_current_active_user

from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized
from modules.Factory.Factory_schemas import Factory, FactoryInDB
from modules.Factory.Factory_services import FactoryService
from shared.utils.service_result import ServiceResult, handle_result
from shared.core.db.db_dependencies import get_database
from typing import List
from modules.users.users.user_schemas import  UserInDB

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=FactoryInDB,name="Factory:create-Factory", status_code=status.HTTP_201_CREATED)
async def create_factory(
    factory: Factory = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "Factory:create-Factory"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await FactoryService(db).create_factory(factory)
        return handle_result(result)



@router.get("/{identifier}",name="Factory:get-Factory-by-identifier", response_model=FactoryInDB,status_code=status.HTTP_200_OK)
async def get_factory_by_identifier(
    identifier: str = Path(..., title="The identifier of the factory to retrieve"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "Factory:get-Factory-by-identifier"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await FactoryService(db).get_factory_by_code(identifier)
        return handle_result(result)


@router.get("/all/", name="Factory:get-all-Factory",response_model=List[FactoryInDB],status_code=status.HTTP_200_OK)
async def get_factory_materials(
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
    ):
    if not is_authorized(current_user, "Factory:get-all-Factory"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await FactoryService(db).get_all_factory()
        return handle_result(result)

@router.delete("/{identifier}", response_model=dict, name="Factory:delete-Factory-by-identifier",status_code=status.HTTP_200_OK)
async def delete_factory_by_identifier(
    identifier: str = Path(..., title="The identifier of the factory to delete"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "Factory:delete-Factory"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await FactoryService(db).delete_factory_by_identifier(identifier)
        return handle_result(result)

@router.put("/{identifier}", response_model=FactoryInDB, name="Factory:update-Factory-by-identifier",status_code=status.HTTP_200_OK)
async def update_factory_by_identifier(
    identifier: str = Path(..., title="The identifier of the factory to update"),
    factory_update: Factory = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
):
    if not is_authorized(current_user, "Factory:update-Factory-by-code"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await FactoryService(db).update_factory_by_code(identifier, factory_update)
        return handle_result(result)