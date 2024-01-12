from fastapi import APIRouter, Body, Depends, Path, status
from databases import Database

from modules.users.auths.auth_dependencies import get_current_active_user

from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized
from modules.Product.Product_schemas import Product, ProductInDB
from modules.Product.Product_services import ProductService
from shared.utils.service_result import ServiceResult, handle_result
from shared.core.db.db_dependencies import get_database
from typing import List,Dict
from modules.users.users.user_schemas import  UserInDB


router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ProductInDB, name="Product:create-Product", status_code=status.HTTP_201_CREATED)
async def create_product(
    product: Product = Body(..., embed=True),  
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Product:create-Product"):
        raise AuthExceptions.AuthUnauthorizedException()
    
    
    result = await ProductService(db).create_product(product,current_user)
    return handle_result(result)



@router.get("/{name}",name="Product:get-Product-by-name", response_model=ProductInDB,status_code=status.HTTP_200_OK)
async def get_product_by_name(
    name: str = Path(..., title="The name of the product to retrieve"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Product:get-Product-by-name"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await ProductService(db).get_product_by_name(name)
        return handle_result(result)


@router.get("/all/", name="Product:get-all-Product",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_product(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Product:get-all-Product"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
       
        result = await ProductService(db).get_all_product( 
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)

@router.delete("/{name}", response_model=dict, name="Product:delete-Product-by-name",status_code=status.HTTP_200_OK)
async def delete_product_by_name(
    name: str = Path(..., title="The name of the product to delete"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Product:delete-Product"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await ProductService(db).delete_product_by_name(name)
        return handle_result(result)

@router.put("/{name}", response_model=ProductInDB, name="Product:update-Product-by-name",status_code=status.HTTP_200_OK)
async def update_product_by_name(
    name: str = Path(..., title="The name of the product to update"),
    product_update: Product = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Product:update-Product-by-name"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await ProductService(db).update_product_by_name(name, product_update,current_user)
        return handle_result(result)