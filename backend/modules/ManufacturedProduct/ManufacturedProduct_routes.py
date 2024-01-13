from fastapi import APIRouter, Body, Depends, Path, status
from databases import Database

from modules.users.auths.auth_dependencies import get_current_active_user

from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized
from modules.ManufacturedProduct.ManufacturedProduct_schemas import ManufacturedProduct, ManufacturedProductInDB
from modules.ManufacturedProduct.ManufacturedProduct_services import ManufacturedProductService
from shared.utils.service_result import ServiceResult, handle_result
from shared.core.db.db_dependencies import get_database
from typing import List,Dict
from modules.users.users.user_schemas import  UserInDB


router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ManufacturedProductInDB, name="ManufacturedProduct:create-ManufacturedProduct", status_code=status.HTTP_201_CREATED)
async def create_manufactured_product(
    id_product: int = Body(..., title="ID of the related product"),
    manufactured_product: ManufacturedProduct = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:create-ManufacturedProduct"):
        raise AuthExceptions.AuthUnauthorizedException()

    manufactured_product.id_product = id_product

    result = await ManufacturedProductService(db).create_manufactured_product(manufactured_product,current_user)
    return handle_result(result)

@router.get("/{lot_number}",name="ManufacturedProduct:get-ManufacturedProduct-by-lot_number", response_model=ManufacturedProductInDB,status_code=status.HTTP_200_OK)
async def get_manufactured_product_by_lot_number(
    lot_number: str = Path(..., title="The lot_number of the manufactured product to retrieve"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:get-ManufacturedProduct-by-lot_number"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await ManufacturedProductService(db).get_manufactured_product_by_lot_number(lot_number)
        return handle_result(result)

@router.get("/all/", name="ManufacturedProduct:get-all-ManufacturedProduct",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_manufactured_product(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:get-all-ManufacturedProduct"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :

        result = await ManufacturedProductService(db).get_all_manufactured_product( 
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)

@router.delete("/{lot_number}", response_model=dict, name="ManufacturedProduct:delete-ManufacturedProduct-by-lot_number",status_code=status.HTTP_200_OK)
async def delete_manufactured_product_by_lot_number(
    lot_number: str = Path(..., title="The lot_number of the manufactured product to delete"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:delete-ManufacturedProduct"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await ManufacturedProductService(db).delete_manufactured_product_by_lot_number(lot_number)
        return handle_result(result)

@router.put("/{lot_number}", response_model=ManufacturedProductInDB, name="ManufacturedProduct:update-ManufacturedProduct-by-lot_number",status_code=status.HTTP_200_OK)
async def update_manufactured_product_by_lot_number(
    id_product: int = Body(..., title="ID of the related product"),
    lot_number: str = Path(..., title="The lot_number of the manufactured product to update"),
    manufactured_product_update: ManufacturedProduct = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:update-ManufacturedProduct-by-lot_number"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        manufactured_product_update.id_product = id_product

        result = await ManufacturedProductService(db).update_manufactured_product_by_lot_number(lot_number, manufactured_product_update,current_user)
        return handle_result(result)