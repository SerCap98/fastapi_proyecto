from fastapi import APIRouter, Body, Depends, Path, Query, status
from databases import Database
from typing import List,Dict
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result

from uuid import UUID
from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized
from modules.users.users.user_schemas import  UserInDB

from modules.RawMaterialOrder.RawMaterialOrder_exceptions import RawMaterialOrderExceptions
from modules.RawMaterialOrder.RawMaterialOrder_services import RawMaterialOrderService
from modules.RawMaterialOrder.RawMaterialOrder_schemas import RawMaterialOrder,RawMaterialOrderInDB, RawMaterialOrderToUpdated

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=RawMaterialOrderInDB, name="RawMaterialOrder:create-raw-material-order", status_code=status.HTTP_201_CREATED)
async def create_raw_material_order(
    RawMaterialOrder: RawMaterialOrder = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "RawMaterialOrder:create-raw-material-order"):
        raise AuthExceptions.AuthUnauthorizedException()

    result = await RawMaterialOrderService(db).create_raw_material_order(RawMaterialOrder,current_user)
    return handle_result(result)

@router.get("/get-order/all/", name="RawMaterialOrder:get-all-order",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_order(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "RawMaterialOrder:get-all-order"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :

        result = await RawMaterialOrderService(db).get_all_order(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)

@router.get("/get-order/{id}",name="RawMaterialOrder:get-order-by-id", response_model=RawMaterialOrderInDB,status_code=status.HTTP_200_OK)
async def get_order_by_id(
    id: UUID = Path(..., title="The id of the order"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "RawMaterialOrder:get-order-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await RawMaterialOrderService(db). get_order_by_id(id)
        return handle_result(result)


@router.put("/update-order/{id}",name="RawMaterialOrder:updated-order", response_model=RawMaterialOrderInDB,status_code=status.HTTP_200_OK)
async def update_order(
    id: UUID = Path(..., title="The id of the order"),
    data: RawMaterialOrderToUpdated = Body(..., title="The new data order"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
) -> ServiceResult:
         if not is_authorized(current_user, "RawMaterialOrder:updated-order"):
            return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
         else :
            result = await RawMaterialOrderService(db).update_order(current_user,data,id)
            return handle_result(result)

@router.put("/set-delivered/{id}",name="RawMaterialOrder:set-delivered", response_model=RawMaterialOrderInDB,status_code=status.HTTP_200_OK)
async def set_delivered(
    id: UUID = Path(..., title="The id of the raw material"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
) -> ServiceResult:
         if not is_authorized(current_user, "RawMaterialOrder:set-delivered"):
            return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
         else :
            result = await RawMaterialOrderService(db).set_delivered(current_user,id)
            return handle_result(result)

@router.delete("/delete-order/{id}",name="RawMaterialOrder:delete-order-by-id", response_model=dict,status_code=status.HTTP_200_OK)
async def delete_order_by_Factory_and_RawMaterial(
    id: UUID = Path(..., title="The id of the order"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "RawMaterialOrder:delete-order-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await RawMaterialOrderService(db).delete_order_by_id(id)
        return handle_result(result)