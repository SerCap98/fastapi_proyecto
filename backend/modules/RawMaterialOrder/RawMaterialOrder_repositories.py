from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository

from modules.RawMaterialOrder.RawMaterialOrder_exceptions import RawMaterialOrderExceptions
from modules.RawMaterialOrder.RawMaterialOrder_schemas import RawMaterialOrder,RawMaterialOrderInDB,RawMaterialOrderList, RawMaterialOrderToUpdated,state1

#import logging
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)

class RawMaterialOrderRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[RawMaterialOrder]:
        return RawMaterialOrder

    @property
    def _schema_out(self) -> Type[RawMaterialOrderInDB]:
        return RawMaterialOrderInDB

    async def create_raw_material_order(self, RawMaterialOrder: RawMaterialOrder,current_user: UserInDB,factory:UUID,raw_material:UUID ) -> RawMaterialOrderInDB:
        from modules.RawMaterialOrder.RawMaterialOrder_sqlstaments import CREATE_RAW_MATERIAL_ORDER

        RawMaterialOrder_id = str(uuid.uuid4())
        current_time = datetime.now()
 
        values = {
            "id": RawMaterialOrder_id ,
            "raw_material": raw_material,
            "factory": factory,
            "quantity":RawMaterialOrder.quantity if RawMaterialOrder.quantity else None,
            "state":state1.ON_HOLD.value,
            "note":RawMaterialOrder.note if RawMaterialOrder.note else None,
            "cost":RawMaterialOrder.cost if RawMaterialOrder.cost else None,
            "delivered":False,
            "date_delivered": None,
            "created_by": current_user.id,
            "created_at": current_time
            }
    
        try:
            record = await self.db.fetch_one(query=CREATE_RAW_MATERIAL_ORDER , values=values)
   
        except Exception as e:
            print(e)
            raise RawMaterialOrderExceptions.RawMaterialOrderInvalidCreateParamsException(e)

        result = record_to_dict(record)
 
        return self._schema_out(**result)

    async def get_all_order(self,
        search: str | None,
        order: str | None,
        direction: str | None
        ) -> List:
        from modules.RawMaterialOrder.RawMaterialOrder_sqlstaments import LIST_RAW_MATERIAL_ORDER,RAW_MATERIAL_ORDER_COMPLEMENTS,RAW_MATERIAL_ORDER_SEARCH

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = RAW_MATERIAL_ORDER_COMPLEMENTS(order, direction)
        sql_search = RAW_MATERIAL_ORDER_SEARCH()
        if not search:
            sql_sentence = LIST_RAW_MATERIAL_ORDER + sql_sentence
        else:
            sql_sentence = LIST_RAW_MATERIAL_ORDER + sql_search + sql_sentence
            values["search"] = "%" + search + "%"
        try:

            records = await self.db.fetch_all(query=sql_sentence,values=values)
            if len(records) == 0 or not records:
                return []
            return [RawMaterialOrderList(**dict(record)) for record in records]

        except Exception as e:

            raise RawMaterialOrderExceptions.RawMaterialOrderException()

    async def get_order_by_id(self,id:UUID ) -> RawMaterialOrderInDB:
        from modules.RawMaterialOrder.RawMaterialOrder_sqlstaments import GET_RAW_MATERIAL_ORDER
        values = {
            "id": id

            }

        record = await self.db.fetch_one(query=GET_RAW_MATERIAL_ORDER, values=values)
        if not record:
            raise RawMaterialOrderExceptions.RawMaterialOrderNotFoundException()
        return self._schema_out(**dict(record))


    async def update_order(self,current_user: UserInDB,new_data:RawMaterialOrderToUpdated ,old_data:RawMaterialOrderInDB) -> RawMaterialOrderInDB:
        from modules.RawMaterialOrder.RawMaterialOrder_sqlstaments import UPDATED_ORDER
        current_time = datetime.now()
        try:
            print(old_data)
            values = {
                "id":old_data.id,
                "quantity":new_data.quantity if new_data.quantity else old_data.quantity,
                "note": new_data.note if new_data.note else old_data.note,
                "cost": new_data.cost if new_data.cost else old_data.cost,
                "updated_by": current_user.id,
                "updated_at": current_time
                }
            print(values)
            record = await self.db.fetch_one(query=UPDATED_ORDER , values=values)
    
        except Exception as e:
            print(e)
            raise RawMaterialOrderExceptions.RawMaterialOrderInvalidUpdateParamsException(e)

        result=self._schema_out(**dict(record))
        return result

    async def set_delivered(self,current_user: UserInDB,id:UUID) -> RawMaterialOrderInDB:
        from modules.RawMaterialOrder.RawMaterialOrder_sqlstaments import SET_DELIVERED_RAW_MATERIAL_ORDER
        current_time = datetime.now()
        try:
            values = {
                "id": id,
                "delivered": True,
                "date_delivered": current_time,
                "updated_by": current_user.id,
                "updated_at": current_time
                }

            record = await self.db.fetch_one(query=SET_DELIVERED_RAW_MATERIAL_ORDER , values=values)
        except Exception as e:
            raise RawMaterialOrderExceptions.RawMaterialOrderInvalidUpdateParamsException(e)

        result=self._schema_out(**dict(record))
        return result

    async def delete_order_by_id(self,id:UUID ) -> bool:
        from modules.RawMaterialOrder.RawMaterialOrder_sqlstaments import DELETE_RAW_MATERIAL_ORDER
        try:
            values = {
                "id": id 
                }

            record = await self.db.fetch_one(query=DELETE_RAW_MATERIAL_ORDER, values=values)
        except Exception as e:
            raise RawMaterialOrderExceptions.RawMaterialOrderDeleteException()
        return True