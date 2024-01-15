
from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository
from modules.WarehouseProductInventory.WarehouseProductInventory_exceptions import WarehouseProductInventoryExceptions
from modules.WarehouseProductInventory.WarehouseProductInventory_schemas import WarehouseProductInventory, WarehouseProductInventoryInDB, WarehouseProductInventoryList, WarehouseProductInventoryListSummary


class WarehouseProductInventoryRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[WarehouseProductInventory]:
        return WarehouseProductInventory

    @property
    def _schema_out(self) -> Type[WarehouseProductInventoryInDB]:
        return WarehouseProductInventoryInDB

    async def create_WarehouseProductInventory(self, WarehouseProductInventory: WarehouseProductInventory,warehouse:UUID,current_user: UserInDB) -> WarehouseProductInventoryInDB:
        from modules.WarehouseProductInventory.WarehouseProductInventory_sqlstaments import CREATE_WAREHOUSE_PRODUCT_INVENTORY

        WarehouseProductInventory_id = str(uuid.uuid4())
        current_time = datetime.now()

        values = {
            "id": WarehouseProductInventory_id ,
            "id_warehouse":warehouse ,
            "id_manufactured_product":WarehouseProductInventory.id_manufactured_product ,
            "available_product":40,
            "created_by": current_user.id,
            "created_at": current_time
        }

        try:

            record = await self.db.fetch_one(query=CREATE_WAREHOUSE_PRODUCT_INVENTORY, values=values)
        except Exception as e:
            raise WarehouseProductInventoryExceptions.WarehouseProductInventoryInvalidCreateParamsException(e=e)

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_warehouse_product_inventory_by_id(self, id: UUID) -> WarehouseProductInventoryInDB:
        from modules.WarehouseProductInventory.WarehouseProductInventory_sqlstaments import GET_WAREHOUSE_PRODUCT_INVENTORY_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_WAREHOUSE_PRODUCT_INVENTORY_BY_ID, values=values)

        if not record:
            raise WarehouseProductInventoryExceptions.WarehouseProductInventoryNotFoundException()
        return self._schema_out(**dict(record))
    
    async def decrease_quantity_available(self,current_user: UserInDB,id: UUID, decrease_quantity: int) -> WarehouseProductInventoryInDB:
        from modules.WarehouseProductInventory.WarehouseProductInventory_sqlstaments import DISCOUNT_WAREHOUSE_PRODUCT_INVENTORY_BY_ID
        current_time = datetime.now()
        try:
            values = {
                "id": id ,
                "decrease_quantity":decrease_quantity,
                "updated_by": current_user.id,
                "updated_at": current_time
                }

            record = await self.db.fetch_one(query=DISCOUNT_WAREHOUSE_PRODUCT_INVENTORY_BY_ID , values=values)
        except Exception as e:
            raise WarehouseProductInventoryExceptions.WarehouseProductInventoryInvalidUpdateParamsException(e)
        
        result=self._schema_out(**dict(record))
        return result
    
    async def transfer_inventory(self,current_user: UserInDB,id: UUID, warehouse: UUID) -> WarehouseProductInventoryInDB:
        from modules.WarehouseProductInventory.WarehouseProductInventory_sqlstaments import TRANSFER_WAREHOUSE_PRODUCT_INVENTORY_BY_ID
        current_time = datetime.now()
        try:
            values = {
                "id": id ,
                "new_warehouse_id":warehouse,
                "updated_by": current_user.id,
                "updated_at": current_time
                }
     
            record = await self.db.fetch_one(query=TRANSFER_WAREHOUSE_PRODUCT_INVENTORY_BY_ID , values=values)
        except Exception as e:
            print(e)
            raise WarehouseProductInventoryExceptions.WarehouseProductInventoryInvalidUpdateParamsException(e)
        
        result=self._schema_out(**dict(record))
        return result   

    async def delete_Inventory(self,id:UUID) -> bool:
        from modules.WarehouseProductInventory.WarehouseProductInventory_sqlstaments import DELETE_WAREHOUSE_PRODUCT_INVENTORY_BY_ID 
        try:
            values = {
                "id": id 
                }

            record = await self.db.fetch_one(query=DELETE_WAREHOUSE_PRODUCT_INVENTORY_BY_ID, values=values)
        except Exception as e:
            raise WarehouseProductInventoryExceptions.WarehouseProductInventoryDeleteException()
        return True 
    
    async def get_all_inventory(self,
        search: str | None,
        order: str | None,
        direction: str | None
        ) -> List:
        from modules.WarehouseProductInventory.WarehouseProductInventory_sqlstaments import LIST_WAREHOUSE_PRODUCT_INVENTORY,WAREHOUSE_PRODUCT_INVENTORY_COMPLEMENTS,WAREHOUSE_PRODUCT_INVENTORY_SEARCH

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = WAREHOUSE_PRODUCT_INVENTORY_COMPLEMENTS(order, direction)
        sql_search = WAREHOUSE_PRODUCT_INVENTORY_SEARCH()
        if not search:
            sql_sentence = LIST_WAREHOUSE_PRODUCT_INVENTORY + sql_sentence
        else:
            sql_sentence = LIST_WAREHOUSE_PRODUCT_INVENTORY + sql_search + sql_sentence
            values["search"] = "%" + search + "%"
        try:
           
            records = await self.db.fetch_all(query=sql_sentence,values=values)
            if len(records) == 0 or not records:
                return []
            return [WarehouseProductInventoryList(**dict(record)) for record in records]
        

        except Exception as e:
            print(e)
            raise WarehouseProductInventoryExceptions.WarehouseProductInventoryListException()

    async def get_all_summary_inventory(self,
        search: str | None,
        order: str | None,
        direction: str | None
        ) -> List:
        from modules.WarehouseProductInventory.WarehouseProductInventory_sqlstaments import LIST_SUMMARY_WAREHOUSE_PRODUCT_INVENTORY,WAREHOUSE_SUMMARY_PRODUCT_INVENTORY_COMPLEMENTS,WAREHOUSE_SUMMARY_PRODUCT_INVENTORY_SEARCH

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_order = WAREHOUSE_SUMMARY_PRODUCT_INVENTORY_COMPLEMENTS(order, direction)
        sql_search = WAREHOUSE_SUMMARY_PRODUCT_INVENTORY_SEARCH(search)

        if search:
            sql_sentence = LIST_SUMMARY_WAREHOUSE_PRODUCT_INVENTORY.format(search_condition=sql_search, order_condition=sql_order)
            values["search"] = f"%{search}%"
        else:
            sql_sentence = LIST_SUMMARY_WAREHOUSE_PRODUCT_INVENTORY.format(search_condition="", order_condition=sql_order)

        try:
           
            records = await self.db.fetch_all(query=sql_sentence,values=values)
            if len(records) == 0 or not records:
                return []
            return [WarehouseProductInventoryListSummary(**dict(record)) for record in records]
        

        except Exception as e:
            print(e)
            raise WarehouseProductInventoryExceptions.WarehouseProductInventoryListException()
