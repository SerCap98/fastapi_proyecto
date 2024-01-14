from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.events import EventBus, InventoryUpdatedEvent
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository

from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_exceptions import FactoryRawMaterialInventoryExceptions
from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_schemas import FactoryRawMaterialInventory,FactoryRawMaterialInventoryInDB,FactoryRawMaterialInventoryList

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
            raise FactoryRawMaterialInventoryExceptions.FactoryRawMaterialException(e)

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
    
    async def increase_quantity_by_factory_and_material(self,current_user: UserInDB,raw_material:UUID ,factory:UUID,increase_quantity:float) -> FactoryRawMaterialInventoryInDB:
        from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_sqlstaments import INCREASE_QUANTITY_FACTORY_RAW_MATERIAL_INVENTORY 
        current_time = datetime.now()
        try:
            values = {
                "factory": factory ,
                "raw_material": raw_material,
                "quantity":increase_quantity,
                "updated_by": current_user.id,
                "updated_at": current_time
                }

            record = await self.db.fetch_one(query=INCREASE_QUANTITY_FACTORY_RAW_MATERIAL_INVENTORY , values=values)
        except Exception as e:
            raise FactoryRawMaterialInventoryExceptions.FactoryRawMaterialException(e)
        
        result=self._schema_out(**dict(record))
        return result
    
    async def decrease_quantity_by_factory_and_material(self,current_user: UserInDB,raw_material:UUID ,factory:UUID,decrease_quantity:float) -> FactoryRawMaterialInventoryInDB:
        from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_sqlstaments import DECREASE_QUANTITY_FACTORY_RAW_MATERIAL_INVENTORY 
        current_time = datetime.now()
        try:
            values = {
                "factory": factory ,
                "raw_material": raw_material,
                "quantity":decrease_quantity,
                "updated_by": current_user.id,
                "updated_at": current_time
                }

            record = await self.db.fetch_one(query=DECREASE_QUANTITY_FACTORY_RAW_MATERIAL_INVENTORY , values=values)
        except Exception as e:
            raise FactoryRawMaterialInventoryExceptions.FactoryRawMaterialException(e)
        result=self._schema_out(**dict(record))
        event = InventoryUpdatedEvent(result.id, result.quantity, result.min_quantity,current_user)
        await EventBus.publish(event)
        return result
    
    async def update_min_quantity_by_factory_and_material(self,current_user: UserInDB,raw_material:UUID ,factory:UUID,new_min_quantity:float) -> FactoryRawMaterialInventoryInDB:
        from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_sqlstaments import UPDATE_MIN_QUANTITY_FACTORY_RAW_MATERIAL_INVENTORY 
        current_time = datetime.now()
        try:
            values = {
                "factory": factory ,
                "raw_material": raw_material,
                "min_quantity":new_min_quantity,
                "updated_by": current_user.id,
                "updated_at": current_time
                }

            record = await self.db.fetch_one(query=UPDATE_MIN_QUANTITY_FACTORY_RAW_MATERIAL_INVENTORY , values=values)
        except Exception as e:
            raise FactoryRawMaterialInventoryExceptions.FactoryRawMaterialException(e)
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
    
    async def get_all_inventory(self,
        search: str | None,
        order: str | None,
        direction: str | None
        ) -> List:
        from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_sqlstaments import LIST_INVENTORY,INVENTORY_COMPLEMENTS,INVENTORY_SEARCH

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = INVENTORY_COMPLEMENTS(order, direction)
        sql_search = INVENTORY_SEARCH()
        if not search:
            sql_sentence = LIST_INVENTORY + sql_sentence
        else:
            sql_sentence = LIST_INVENTORY + sql_search + sql_sentence
            values["search"] = "%" + search + "%"
        try:
           
            records = await self.db.fetch_all(query=sql_sentence,values=values)
            if len(records) == 0 or not records:
                return []
            return [FactoryRawMaterialInventoryList(**dict(record)) for record in records]
        

        except Exception as e:
           
            raise FactoryRawMaterialInventoryExceptions.InventoryListException()
        
    async def get_inventory_by_fact_identifier(self, identifier: str, order: str | None, direction: str | None) -> List:
        from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_sqlstaments import  LIST_INVENTORY_BY_IDENTIFIER,INVENTORY_COMPLEMENTS

        order = order.lower() if order else None
        direction = direction.upper() if direction else None
        sql_sentence = INVENTORY_COMPLEMENTS(order, direction)

        values = {"identifier": identifier.upper()}
        sql_sentence = LIST_INVENTORY_BY_IDENTIFIER + sql_sentence

        try:
            records = await self.db.fetch_all(query=sql_sentence, values=values)
            if not records:
                return []

            return [FactoryRawMaterialInventoryList(**dict(record)) for record in records]

        except Exception as e:
            raise FactoryRawMaterialInventoryExceptions.FactoryRawMaterialException(e)

    async def get_inventory_by_mat_code(self, code: str, order: str | None, direction: str | None) -> List:
        from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_sqlstaments import  LIST_INVENTORY_BY_CODE,INVENTORY_COMPLEMENTS

        order = order.lower() if order else None
        direction = direction.upper() if direction else None
        sql_sentence = INVENTORY_COMPLEMENTS(order, direction)

        values = {"code": code.upper()}
        sql_sentence = LIST_INVENTORY_BY_CODE + sql_sentence

        try:
            records = await self.db.fetch_all(query=sql_sentence, values=values)
            if not records:
                return []

            return [FactoryRawMaterialInventoryList(**dict(record)) for record in records]

        except Exception as e:
            raise FactoryRawMaterialInventoryExceptions.FactoryRawMaterialException(e)