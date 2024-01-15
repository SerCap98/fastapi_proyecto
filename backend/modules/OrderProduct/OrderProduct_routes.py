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

