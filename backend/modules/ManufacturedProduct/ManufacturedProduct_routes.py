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


#GET BY ID PRODUCT
@router.get("/get-manufactured_product-by-id-product",name="ManufacturedProduct:get-manufactured-product-by-id-product", response_model=ManufacturedProductInDB,status_code=status.HTTP_200_OK)
async def get_manufactured_product_by_id_product(
    product_name: str = Query(..., title="The name of the product"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:get-manufactured-product-by-id-product"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await ManufacturedProductService(db).get_manufactured_product_by_id_product(product_name)
        return handle_result(result)

#GET BY ID LOT NUMBER
@router.get("/get-manufactured_product-by-lot-number",name="ManufacturedProduct:get-manufactured-product-by-lot-number", response_model=ManufacturedProductInDB,status_code=status.HTTP_200_OK)
async def get_manufactured_product_by_lot_number(
    lot_number: str = Query(..., title="The lot number"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:get-manufactured-product-by-lot-number"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await ManufacturedProductService(db).get_manufactured_product_by_lot_number(lot_number)
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

#UPDATE BY ID PRODUCT
@router.put("/update-quantity-by-id-product",name="ManufacturedProduct:update-quantity-manufactured-product-by-id-product", response_model=ManufacturedProductInDB,status_code=status.HTTP_200_OK)
async def update_quantity_by_id_product(
    product_name: str = Query(..., title="The name of the product"),
    new_quantity: float= Query(..., title="The amount"), 
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
) -> ServiceResult:
         if not is_authorized(current_user, "ManufacturedProduct:update-quantity-manufactured_product-by-id-product"):
            return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
         else :
            result = await ManufacturedProductService(db).update_quantity_by_id_product(current_user,product_name,new_quantity)
            return handle_result(result)

#UPDATE BY LOT NUMBER
@router.put("/update-quantity-by-lot-number",name="ManufacturedProduct:update-quantity-manufactured-product-by-lot-number", response_model=ManufacturedProductInDB,status_code=status.HTTP_200_OK)
async def update_quantity_by_lot_number(
    lot_number: str = Query(..., title="The lot number"),
    new_quantity: float= Query(..., title="The amount"), 
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
) -> ServiceResult:
         if not is_authorized(current_user, "ManufacturedProduct:update-quantity-manufactured_product-by-lot-number"):
            return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
         else :
            result = await ManufacturedProductService(db).update_quantity_by_lot_number(current_user,lot_number,new_quantity)
            return handle_result(result)

#DELETE BY ID PRODUCT
@router.delete("/delete-manufactured-product-by-id_product",name="ManufacturedProduct:delete-manufactured_product-by-id-product", response_model=dict,status_code=status.HTTP_200_OK)
async def delete_manufactured_product_by_id_product(
    product_name: str = Query(..., title="The name of the product"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:delete-manufactured_product-by-id-product"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await ManufacturedProductService(db).delete_manufactured_product_by_id_product(product_name)
        return handle_result(result)

#DELETE BY LOT NUMBER
@router.delete("/delete-manufactured-product-by-lot-number",name="ManufacturedProduct:delete-manufactured_product-by-lot-number", response_model=dict,status_code=status.HTTP_200_OK)
async def delete_manufactured_product_by_lot_number(
    lot_number: str = Query(..., title="The lot_number"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "ManufacturedProduct:delete-manufactured_product-by-lot-number"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await ManufacturedProductService(db).delete_manufactured_product_by_lot_number(lot_number)
        return handle_result(result)