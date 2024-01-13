from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository

from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_exceptions import FactoryRawMaterialInventoryExceptions
from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_schemas import FactoryRawMaterialInventory,FactoryRawMaterialInventoryInDB

#import logging
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)


class FactoryRawMaterialInventoryRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[FactoryRawMaterialInventory]:
        return FactoryRawMaterialInventory

    @property
    def _schema_out(self) -> Type[FactoryRawMaterialInventoryInDB]:
        return FactoryRawMaterialInventoryInDB

    async def create_Factory_RawMaterial_Inventory(self, FactRawMatInv: FactoryRawMaterialInventory,current_user: UserInDB,raw_material:UUID ,factory:UUID) -> FactoryRawMaterialInventoryInDB:

        from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_sqlstaments import CREATE_FACTORY_RAW_MATERIAL_INVENTORY
       
        
        FactoryRawMaterialInventory_id = str(uuid.uuid4())
        current_time = datetime.now()

        values = {
            "id": FactoryRawMaterialInventory_id ,
            "factory": factory ,
            "raw_material": raw_material ,
            "min_quantity":FactRawMatInv.min_quantity if FactRawMatInv.min_quantity else 0,
            "quantity":FactRawMatInv.quantity if FactRawMatInv.quantity else None,
            "created_by": current_user.id,
            "created_at": current_time
            }
        
        try:
            record = await self.db.fetch_one(query=CREATE_FACTORY_RAW_MATERIAL_INVENTORY , values=values)

        except Exception as e:
            raise FactoryRawMaterialInventoryExceptions.FactoryRawMaterialException(e=e)

        result = record_to_dict(record)
        return self._schema_out(**result)
    
    async def get_inventory_by_Factory_and_RawMaterial(self,raw_material:UUID ,factory:UUID) -> FactoryRawMaterialInventoryInDB:
        from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_sqlstaments import GET_FACTORY_RAW_MATERIAL_INVENTORY 
        values = {
            "factory": factory ,
            "raw_material": raw_material
            }

        record = await self.db.fetch_one(query=GET_FACTORY_RAW_MATERIAL_INVENTORY, values=values)
        if not record:
            raise FactoryRawMaterialInventoryExceptions.FactoryRawMaterialNotFoundException()
        return self._schema_out(**dict(record))
    
    async def delete_inventory_by_Factory_and_RawMaterial(self,raw_material:UUID ,factory:UUID) -> bool:
        from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_sqlstaments import DELETE_FACTORY_RAW_MATERIAL_INVENTORY 
        try:
            values = {
                "factory": factory ,
                "raw_material": raw_material
                }

            record = await self.db.fetch_one(query=DELETE_FACTORY_RAW_MATERIAL_INVENTORY, values=values)
        except Exception as e:
            raise FactoryRawMaterialInventoryExceptions.FactoryRawMaterialDeleteException()
        return True