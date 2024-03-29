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

from modules.ManufacturedProduct.ManufacturedProduct_exceptions import ManufacturedProductExceptions
from modules.ManufacturedProduct.ManufacturedProduct_services import ManufacturedProductService
from modules.ManufacturedProduct.ManufacturedProduct_schemas import ManufacturedProduct,ManufacturedProductInDB

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ManufacturedProductInDB, name="ManufacturedProduct:create-ManufacturedProduct", status_code=status.HTTP_201_CREATED)
async def create_manufactured_product(
   ManufacturedProduct: ManufacturedProduct = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:create-ManufacturedProduct"):
        raise AuthExceptions.AuthUnauthorizedException()

    result = await ManufacturedProductService(db).create_manufactured_product(ManufacturedProduct,current_user)
    return handle_result(result)

@router.get("/get-manufactured_product/all/", name="ManufacturedProduct:get-all-manufactured-product",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_manufactured_product(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:get-all-manufactured-product"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await ManufacturedProductService(db).get_all_manufactured_product(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)

@router.get("/{id}", response_model=ManufacturedProductInDB, name="ManufacturedProduct:get-manufactured-product-by-id")
async def get_manufactured_product_by_id(
    id: UUID = Path(..., title="The id of the manufactured product"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:get-manufactured-product-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await ManufacturedProductService(db).get_manufactured_product_by_id(id)
        return handle_result(result)



@router.delete("/{id}", response_model=UUID, name="ManufacturedProduct:delete-manufactured-product-by-id", status_code=status.HTTP_200_OK)
async def delete_manufactured_product_by_id(
    id: UUID = Path(..., title="The id of the manufactured product"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:delete-manufactured-product-by-id"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))

    result = await ManufacturedProductService(db).delete_manufactured_product_by_id(id=id)
    return handle_result(result)
