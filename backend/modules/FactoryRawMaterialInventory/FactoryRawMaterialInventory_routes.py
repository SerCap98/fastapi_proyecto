from fastapi import APIRouter, Body, Depends, Path, Query, status
from databases import Database
from typing import List,Dict
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result


from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized
from modules.users.users.user_schemas import  UserInDB

from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_exceptions import FactoryRawMaterialInventoryExceptions
from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_services import FactoryRawMaterialInventoryService
from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_schemas import FactoryRawMaterialInventory,FactoryRawMaterialInventoryInDB

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=FactoryRawMaterialInventoryInDB, name="Fact-Mat-Inv:create-Factory-RawMaterial-Inventory", status_code=status.HTTP_201_CREATED)
async def create_Factory_RawMaterial_Inventory(
    FactRawMatInv: FactoryRawMaterialInventory = Body(..., embed=True),  
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Fact-Mat-Inv:create-Factory-RawMaterial-Inventory"):
        raise AuthExceptions.AuthUnauthorizedException()
    
    
    result = await FactoryRawMaterialInventoryService(db).create_Factory_RawMaterial_Inventory(FactRawMatInv,current_user)
    return handle_result(result)

@router.get("/get-inventory",name="Fact-Mat-Inv:get-inventory-by-factory-and-material", response_model=FactoryRawMaterialInventoryInDB,status_code=status.HTTP_200_OK)

async def get_inventory_by_factory_and_material(
    factory_identifier: str = Query(..., title="The identifier of the factory"),
    raw_material_code: str = Query(..., title="The code of the raw material"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Fact-Mat-Inv:get-inventory-by-factory-and-material"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await FactoryRawMaterialInventoryService(db).get_inventory_by_Factory_and_material(factory_identifier, raw_material_code)
        return handle_result(result)

@router.get("/get-inventory/all/", name="Fact-Mat-Inv:get-all-inventory",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_inventory(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Fact-Mat-Inv:get-all-inventory"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
       
        result = await FactoryRawMaterialInventoryService(db).get_all_inventory( 
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)

@router.put("/increase-quantity",name="Fact-Mat-Inv:increase-quantity-inventory-by-factory-and-material", response_model=FactoryRawMaterialInventoryInDB,status_code=status.HTTP_200_OK)
async def update_quantity(
    factory_identifier: str = Query(..., title="The identifier of the factory"),
    raw_material_code: str = Query(..., title="The code of the raw material"),
    increase_quantity: float= Query(..., title="The amount to increase"), 
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
) -> ServiceResult:
         if not is_authorized(current_user, "Fact-Mat-Inv:increase-quantity-inventory-by-factory-and-material"):
            return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
         else :
            result = await FactoryRawMaterialInventoryService(db).increase_quantity_by_factory_and_material(current_user,factory_identifier, raw_material_code,increase_quantity)
            return handle_result(result)
         
@router.put("/decrease-quantity",name="Fact-Mat-Inv:decrease-quantity-inventory-by-factory-and-material", response_model=FactoryRawMaterialInventoryInDB,status_code=status.HTTP_200_OK)
async def update_quantity(
    factory_identifier: str = Query(..., title="The identifier of the factory"),
    raw_material_code: str = Query(..., title="The code of the raw material"),
    decrease_quantity: float= Query(..., title="The amount to decrease"), 
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
) -> ServiceResult:
         if not is_authorized(current_user, "Fact-Mat-Inv:decrease-quantity-inventory-by-factory-and-material"):
            return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
         else :
            result = await FactoryRawMaterialInventoryService(db).decrease_quantity_by_factory_and_material(current_user,factory_identifier, raw_material_code,decrease_quantity)
            return handle_result(result)

@router.delete("/delete-inventory",name="Fact-Mat-Inv:delete-Inventory-by-factory-and-material", response_model=dict,status_code=status.HTTP_200_OK)

async def delete_Factory_RawMaterial_Inventory(
    factory_identifier: str = Query(..., title="The identifier of the factory"),
    raw_material_code: str = Query(..., title="The code of the raw material"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Fact-Mat-Inv:delete-Inventory-by-factory-and-material"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await FactoryRawMaterialInventoryService(db).delete_inventory_by_factory_and_material(factory_identifier, raw_material_code)
        return handle_result(result)