from uuid import UUID
from fastapi import APIRouter, Body, Depends, Path, Query, status
from databases import Database
from typing import List,Dict
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result

from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized
from modules.users.users.user_schemas import  UserInDB

from modules.OrderProduct.OrderProduct_exceptions import OrderProductExceptions
from modules.OrderProduct.OrderProduct_services import OrderProductService
from modules.OrderProduct.OrderProduct_schemas import OrderProduct,OrderProductInDB

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=OrderProductInDB, name="OrderProduct:create-order-product", status_code=status.HTTP_201_CREATED)
async def create_order_product(
    OrderProduct: OrderProduct = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "OrderProduct:create-order-product"):
        raise AuthExceptions.AuthUnauthorizedException()

    result = await OrderProductService(db).create_order_product(OrderProduct,current_user)
    return handle_result(result)

@router.get("/get-order",name="OrderProduct:get-order-by-product", response_model=OrderProductInDB,status_code=status.HTTP_200_OK)
async def get_order_by_product(
    product_name: str = Query(..., title="The name of the product"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "OrderProduct:get-order-by-product"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await OrderProductService(db).get_order_by_product(product_name)
        return handle_result(result)

@router.get("/get-order_product/all/", name="OrderProduct:get-all-OrdersProduct",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_order_product(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "OrderProduct:get-all-OrdersProduct"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await OrderProductService(db).get_all_order_product(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)

@router.delete("/delete-order",name="OrderProduct:delete-order", response_model=dict,status_code=status.HTTP_200_OK)
async def delete_order(
    product_name: str = Query(..., title="The name of the product"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "OrderProduct:delete-order"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await OrderProductService(db).delete_order(product_name)
        return handle_result(result)
