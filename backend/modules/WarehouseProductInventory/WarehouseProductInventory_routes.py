from fastapi import APIRouter, Body, Depends, Path, Query, status
from databases import Database
from shared.utils.verify_auth import is_authorized
from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from uuid import UUID

from modules.WarehouseProductInventory.WarehouseProductInventory_schemas import WarehouseProductInventory, WarehouseProductInventoryInDB, WarehouseProductInventoryList
from modules.WarehouseProductInventory.WarehouseProductInventory_services import WarehouseProductInventoryServices

from shared.utils.service_result import ServiceResult, handle_result
from shared.core.db.db_dependencies import get_database
from typing import List,Dict
from modules.users.users.user_schemas import  UserInDB


router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=WarehouseProductInventoryInDB, name="WarehouseProductInventory:create-Warehouse-Product-Inventory", status_code=status.HTTP_201_CREATED)
async def create_WarehouseProductInventory(
    warehouse: WarehouseProductInventory = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "WarehouseProductInventory:create-Warehouse-Product-Inventory"):
        raise AuthExceptions.AuthUnauthorizedException()

    result = await WarehouseProductInventoryServices(db).create_WarehouseProductInventory(warehouse,current_user)
    return handle_result(result)


@router.get("/{id}", response_model=WarehouseProductInventoryInDB, name="WarehouseProductInventory:get-Warehouse-Product-Inventory")
async def get_warehouse_product_inventory_by_id(
    id: UUID = Path(..., title="The id of the record"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
) -> ServiceResult:
    if not is_authorized(current_user, "WarehouseProductInventory:get-Warehouse-Product-Inventory"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await WarehouseProductInventoryServices(db).get_warehouse_product_inventory_by_id(id)
        return handle_result(result)
    
@router.put("/decrease-quantity-available",name="WarehouseProductInventory:decrease-quantity-available", response_model=WarehouseProductInventoryInDB,status_code=status.HTTP_200_OK)
async def decrease_quantity_available(
    id: UUID = Query(..., title="The id of the inventory"),
    decrease_quantity: int = Query(..., title="The quantity to decrease"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
) -> ServiceResult:
         if not is_authorized(current_user, "WarehouseProductInventory:decrease-quantity-available"):
            return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
         else :
            result = await WarehouseProductInventoryServices(db).decrease_quantity_available(current_user,id, decrease_quantity)
            return handle_result(result)
         
@router.put("/transfer-inventory",name="WarehouseProductInventory:transfer-inventory", response_model=WarehouseProductInventoryInDB,status_code=status.HTTP_200_OK)
async def transfer_inventory(
    id: UUID = Query(..., title="The id of the inventory"),
    new_warehouse: str = Query(..., title="The name of the new warehouse"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
) -> ServiceResult:
         if not is_authorized(current_user, "WarehouseProductInventory:transfer-inventory"):
            return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
         else :
            result = await WarehouseProductInventoryServices(db).transfer_inventory(current_user,id, new_warehouse)
            return handle_result(result)
         
@router.delete("/delete-inventory",name="WarehouseProductInventory:delete-inventory", response_model=dict,status_code=status.HTTP_200_OK)

async def delete_Inventory(
    id: UUID = Query(..., title="The id of the inventory"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "WarehouseProductInventory:delete-inventory"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await WarehouseProductInventoryServices(db).delete_Inventory(id)
        return handle_result(result)
    

@router.get("/get-inventory/all/", name="WarehouseProductInventory:get-all-inventory",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_inventory(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "WarehouseProductInventory:get-all-inventory"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
       
        result = await WarehouseProductInventoryServices(db).get_all_inventory( 
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)
    
@router.get("/get-inventory/all-summary/", name="WarehouseProductInventory:get-all-summary-inventory",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_summary_inventory(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "WarehouseProductInventory:get-all-summary-inventory"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
       
        result = await WarehouseProductInventoryServices(db).get_all_summary_inventory( 
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)