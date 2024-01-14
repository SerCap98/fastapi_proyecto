from fastapi import APIRouter, Body, Depends, Path, status
from databases import Database

from modules.users.auths.auth_dependencies import get_current_active_user

from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized
from modules.Warehouse.Warehouse_schemas import Warehouse, WarehouseInDB
from modules.Warehouse.Warehouse_services import WarehouseService
from shared.utils.service_result import ServiceResult, handle_result
from shared.core.db.db_dependencies import get_database
from typing import List,Dict
from modules.users.users.user_schemas import  UserInDB


router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=WarehouseInDB, name="Warehouse:create-Warehouse", status_code=status.HTTP_201_CREATED)
async def create_warehouse(
    warehouse: Warehouse = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Warehouse:create-Warehouse"):
        raise AuthExceptions.AuthUnauthorizedException()

    result = await WarehouseService(db).create_warehouse(warehouse,current_user)
    return handle_result(result)


@router.get("/{name}",name="Warehouse:get-Warehouse-by-name", response_model=WarehouseInDB,status_code=status.HTTP_200_OK)
async def get_warehouse_by_name(
    name: str = Path(..., title="The name of the warehouse"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Warehouse:get-Warehouse-by-name"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await WarehouseService(db).get_warehouse_by_name(name)
        return handle_result(result)


@router.get("/all/", name="Warehouse:get-all-Warehouse",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_warehouse(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Warehouse:get-all-Warehouse"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :

        result = await WarehouseService(db).get_all_warehouse(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)

@router.delete("/{name}", response_model=dict, name="Warehouse:delete-Warehouse-by-name",status_code=status.HTTP_200_OK)
async def delete_warehouse_by_name(
    name: str = Path(..., title="The code of the warehouse to delete"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Warehouse:delete-Warehouse"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await WarehouseService(db).delete_warehouse_by_name(name)
        return handle_result(result)

@router.put("/{name}", response_model=WarehouseInDB, name="Warehouse:update-Warehouse-by-name",status_code=status.HTTP_200_OK)
async def update_warehouse_by_name(
    name: str = Path(..., title="The name of the warehouse"),
    warehouse_update: Warehouse = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Warehouse:update-Warehouse-by-name"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await WarehouseService(db).update_warehouse_by_name(name, warehouse_update,current_user)
        return handle_result(result)