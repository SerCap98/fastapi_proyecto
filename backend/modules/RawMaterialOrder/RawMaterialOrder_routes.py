from fastapi import APIRouter, Body, Depends, Path, Query, status
from databases import Database
from typing import List,Dict
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result


from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized
from modules.users.users.user_schemas import  UserInDB

from modules.RawMaterialOrder.RawMaterialOrder_exceptions import RawMaterialOrderExceptions
from modules.RawMaterialOrder.RawMaterialOrder_services import RawMaterialOrderService
from modules.RawMaterialOrder.RawMaterialOrder_schemas import RawMaterialOrder,RawMaterialOrderInDB

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

@router.put("/increase-quantity",name="RawMaterialOrder:increase-quantity-order-by-factory-and-material", response_model=RawMaterialOrderInDB,status_code=status.HTTP_200_OK)
async def increase_quantity(
    raw_material_code: str = Query(..., title="The code of the raw material"),
    factory_identifier: str = Query(..., title="The identifier of the factory"),
    increase_quantity: float= Query(..., title="The amount to increase"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
) -> ServiceResult:
         if not is_authorized(current_user, "RawMaterialOrder:increase-quantity-order-by-factory-and-material"):
            return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
         else :
            result = await RawMaterialOrderService(db).increase_quantity_by_factory_and_material(current_user,factory_identifier, raw_material_code,increase_quantity)
            return handle_result(result)

@router.put("/decrease-quantity",name="RawMaterialOrder:decrease-quantity-order-by-factory-and-material", response_model=RawMaterialOrderInDB,status_code=status.HTTP_200_OK)
async def decrease_quantity(
    raw_material_code: str = Query(..., title="The code of the raw material"),
    factory_identifier: str = Query(..., title="The identifier of the factory"),
    decrease_quantity: float= Query(..., title="The amount to decrease"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
) -> ServiceResult:
         if not is_authorized(current_user, "RawMaterialOrder:decrease-quantity-order-by-factory-and-material"):
            return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
         else :
            result = await RawMaterialOrderService(db).decrease_quantity_by_factory_and_material(current_user,factory_identifier, raw_material_code,decrease_quantity)
            return handle_result(result)

@router.delete("/delete-order",name="RawMaterialOrder:delete-order-by-factory-and-material", response_model=dict,status_code=status.HTTP_200_OK)
async def delete_order_by_Factory_and_RawMaterial(
    factory_identifier: str = Query(..., title="The identifier of the factory"),
    raw_material_code: str = Query(..., title="The code of the raw material"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "RawMaterialOrder:delete-order-by-factory-and-material"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await RawMaterialOrderService(db).delete_order_by_Factory_and_RawMaterial(factory_identifier, raw_material_code)
        return handle_result(result)