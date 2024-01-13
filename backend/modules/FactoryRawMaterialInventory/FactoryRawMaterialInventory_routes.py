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

@router.post("/", response_model=FactoryRawMaterialInventoryInDB, name="FactRawMatInv:create-Factory_RawMaterial_Inventory", status_code=status.HTTP_201_CREATED)
async def create_Factory_RawMaterial_Inventory(
    FactRawMatInv: FactoryRawMaterialInventory = Body(..., embed=True),  
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "RawMaterial:create-Factory-RawMaterial-Inventory"):
        raise AuthExceptions.AuthUnauthorizedException()
    
    
    result = await FactoryRawMaterialInventoryService(db).create_Factory_RawMaterial_Inventory(FactRawMatInv,current_user)
    return handle_result(result)

@router.get("/get-inventory",name="FactRawMatInv:get-Factory-RawMaterial-Inventory-by-factory-and-RawMaterial", response_model=FactoryRawMaterialInventoryInDB,status_code=status.HTTP_200_OK)

async def get_Factory_RawMaterial_Inventory(
    factory_identifier: str = Query(..., title="The identifier of the factory"),
    raw_material_code: str = Query(..., title="The code of the raw material"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "RawMaterial:get-Inventory-by-factory-and-RawMaterial"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await FactoryRawMaterialInventoryService(db).get_inventory_by_Factory_and_RawMaterial(factory_identifier, raw_material_code)
        return handle_result(result)

@router.delete("/delete-inventory",name="FactRawMatInv:delete-Factory-RawMaterial-Inventory-by-factory-and-RawMaterial", response_model=dict,status_code=status.HTTP_200_OK)

async def delete_Factory_RawMaterial_Inventory(
    factory_identifier: str = Query(..., title="The identifier of the factory"),
    raw_material_code: str = Query(..., title="The code of the raw material"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "RawMaterial:delete-Inventory-by-factory-and-RawMaterial"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await FactoryRawMaterialInventoryService(db).delete_inventory_by_Factory_and_RawMaterial(factory_identifier, raw_material_code)
        return handle_result(result)