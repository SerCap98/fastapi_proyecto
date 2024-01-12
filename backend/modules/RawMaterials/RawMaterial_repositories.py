
from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB

from modules.RawMaterials.RawMaterial_exceptions import RawMaterialExceptions
from modules.RawMaterials.RawMaterial_schemas import RawMaterial,RawMaterialInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class RawMaterialRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[RawMaterial]:
        return RawMaterial

    @property
    def _schema_out(self) -> Type[RawMaterialInDB]:
        return RawMaterialInDB

    async def create_raw_material(self, raw_material: RawMaterial,current_user: UserInDB) -> RawMaterialInDB:
        from modules.RawMaterials.RawMaterial_sqlstaments import CREATE_RAW_MATERIAL
       
        raw_material_id = str(uuid.uuid4())
        current_time = datetime.now()
        print(raw_material_id)
        
        values = {
            "id": raw_material_id ,
            "name": raw_material.name.upper() if raw_material.name else None,
            "code": raw_material.code.upper() if raw_material.code else None,
            "created_by": current_user.id,
            "created_at": current_time
            }
        print(values)
        try:
            print(values)
            record = await self.db.fetch_one(query=CREATE_RAW_MATERIAL, values=values)
        except Exception as e:
            raise RawMaterialExceptions.RawMaterialInvalidCreateParamsException(e=e)

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_raw_material_by_code(self, code: str) -> RawMaterialInDB:
        from modules.RawMaterials.RawMaterial_sqlstaments import GET_RAW_MATERIAL_BY_CODE
        values = {"code": code}
        record = await self.db.fetch_one(query=GET_RAW_MATERIAL_BY_CODE, values=values)
        if not record:
            raise RawMaterialExceptions.RawMaterialNotFoundException()
        return self._schema_out(**dict(record))

    async def update_raw_material_by_code(self, exist_raw_material: ServiceResult, raw_material_update: RawMaterial,current_user: UserInDB) -> RawMaterialInDB:
        from modules.RawMaterials.RawMaterial_sqlstaments import UPDATE_RAW_MATERIAL_BY_CODE

        updated_values = {
            "name": raw_material_update.name.upper() if raw_material_update.name else exist_raw_material.value.name,
            "code": raw_material_update.code.upper() if raw_material_update.code else exist_raw_material.value.code,
            "updated_by": current_user.id,
            "updated_at": datetime.now()
        }
        try:
            record = await self.db.fetch_one(query=UPDATE_RAW_MATERIAL_BY_CODE, values={**updated_values, "original_code": exist_raw_material.value.code})
            
            return self._schema_out(**dict(record))
        except Exception as e:
            raise RawMaterialExceptions.RawMaterialInvalidUpdateParamsException(e=e)

    async def delete_raw_material_by_code(self, code: str):
        from modules.RawMaterials.RawMaterial_sqlstaments import DELETE_RAW_MATERIAL_BY_CODE
        try:
            await self.db.execute(query=DELETE_RAW_MATERIAL_BY_CODE, values={"code": code.upper()})
        except Exception as e:
            raise RawMaterialExceptions.RawMaterialDeletionException()
        return True

    async def get_all_raw_material(self,
        search: str | None,
        order: str | None,
        direction: str | None
        ) -> List:
        
        from modules.RawMaterials.RawMaterial_sqlstaments import LIST_RAW_MATERIALS,RAW_MATERIALS_COMPLEMENTS,RAW_MATERIALS_SEARCH

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = RAW_MATERIALS_COMPLEMENTS(order, direction)
        sql_search = RAW_MATERIALS_SEARCH()
        if not search:
            sql_sentence = LIST_RAW_MATERIALS + sql_sentence
        else:
            sql_sentence = LIST_RAW_MATERIALS + sql_search + sql_sentence
            values["search"] = "%" + search + "%"
        try:
           
            records = await self.db.fetch_all(query=sql_sentence,values=values)
            if len(records) == 0 or not records:
                return []

            return [self._schema_out(**dict(record)) for record in records]
        

        except Exception as e:
            raise RawMaterialExceptions.RawMaterialListException