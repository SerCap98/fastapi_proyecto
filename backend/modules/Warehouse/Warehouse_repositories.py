
from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB

from modules.Warehouse.Warehouse_exceptions import WarehouseExceptions
from modules.Warehouse.Warehouse_schemas import Warehouse,WarehouseInDB, WarehouseList, type1
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository

class WarehouseRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[Warehouse]:
        return Warehouse

    @property
    def _schema_out(self) -> Type[WarehouseInDB]:
        return WarehouseInDB

    async def create_warehouse(self, warehouse: Warehouse,current_user: UserInDB) -> WarehouseInDB:
        from modules.Warehouse.Warehouse_sqlstaments import CREATE_WAREHOUSE

        warehouse_id = str(uuid.uuid4())
        current_time = datetime.now()

        values = {
            "id": warehouse_id ,
            "name": warehouse.name.upper() if warehouse.name else None,
            "type": warehouse.type.name if warehouse.type else None,
            "type_num": warehouse.type_num if warehouse.type_num else None,
            "created_by": current_user.id,
            "created_at": current_time
            }

        try:

            record = await self.db.fetch_one(query=CREATE_WAREHOUSE, values=values)
        except Exception as e:
            raise WarehouseExceptions.WarehouseInvalidCreateParamsException(e=e)

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_warehouse_by_name(self, name: str) -> WarehouseInDB:
        from modules.Warehouse.Warehouse_sqlstaments import GET_WAREHOUSE_BY_NAME
        values = {"name": name.upper()}
        record = await self.db.fetch_one(query=GET_WAREHOUSE_BY_NAME, values=values)
        if not record:
            raise WarehouseExceptions.WarehouseNotFoundException()
        return self._schema_out(**dict(record))

    async def update_warehouse_by_name(self, exist_warehouse: ServiceResult, warehouse_update: Warehouse,current_user: UserInDB) -> WarehouseInDB:
        from modules.Warehouse.Warehouse_sqlstaments import UPDATE_WAREHOUSE_BY_NAME

        updated_values = {
            "name": warehouse_update.name.upper() if warehouse_update.name else exist_warehouse.value.name,
            "type": warehouse_update.type.name if warehouse_update.type else exist_warehouse.type,
            "type_num": warehouse_update.type_num if warehouse_update.type_num else exist_warehouse.value.type_num,
            "updated_by": current_user.id,
            "updated_at": datetime.now()
        }
        try:
            record = await self.db.fetch_one(query=UPDATE_WAREHOUSE_BY_NAME, values={**updated_values, "original_name": exist_warehouse.value.name.upper()})

            return self._schema_out(**dict(record))
        except Exception as e:
            raise WarehouseExceptions.WarehouseInvalidUpdateParamsException(e=e)

    async def delete_warehouse_by_name(self, name: str) -> bool:
        from modules.Warehouse.Warehouse_sqlstaments import DELETE_WAREHOUSE_BY_NAME
        try:
            await self.db.execute(query=DELETE_WAREHOUSE_BY_NAME, values={"name": name.upper()})
        except Exception as e:
            raise WarehouseExceptions.WarehouseDeletionException()
        return True

    async def get_all_warehouse(self,
        search: str | None,
        order: str | None,
        direction: str | None
        ) -> List:

        from modules.Warehouse.Warehouse_sqlstaments import LIST_WAREHOUSE,WAREHOUSE_COMPLEMENTS,WAREHOUSE_SEARCH

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = WAREHOUSE_COMPLEMENTS(order, direction)
        sql_search = WAREHOUSE_SEARCH()
        if not search:
            sql_sentence = LIST_WAREHOUSE + sql_sentence
        else:
            sql_sentence = LIST_WAREHOUSE + sql_search + sql_sentence
            values["search"] = "%" + search + "%"
        try:

            records = await self.db.fetch_all(query=sql_sentence,values=values)
            if len(records) == 0 or not records:
                return []

            return [WarehouseList(**dict(record)) for record in records]

        except Exception as e:
            raise WarehouseExceptions.WarehouseListException