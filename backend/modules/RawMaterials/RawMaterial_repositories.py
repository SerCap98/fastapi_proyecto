
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
        raw_material.name = raw_material.name.upper()
        raw_material.code = raw_material.code.upper()

        values = {
            "id": raw_material_id,
            "name": raw_material.name,
            "code": raw_material.code,
            "created_by": current_user.id,
            "created_at": current_time
        }

        try:
            record = await self.db.fetch_one(query=CREATE_RAW_MATERIAL, values=values)
        except Exception as e:
            raise RawMaterialExceptions.RawMaterialCreationException()

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
            raise RawMaterialExceptions.RawMaterialUpdateException()

    async def delete_raw_material_by_code(self, code: str):
        from modules.RawMaterials.RawMaterial_sqlstaments import DELETE_RAW_MATERIAL_BY_CODE
        try:
            await self.db.execute(query=DELETE_RAW_MATERIAL_BY_CODE, values={"code": code.upper()})
        except Exception as e:
            raise RawMaterialExceptions.RawMaterialDeletionException()
        return True

    async def get_all_raw_material(self) -> List[RawMaterialInDB]:
        
        from modules.RawMaterials.RawMaterial_sqlstaments import LIST_RAW_MATERIALS
    
        try:
            records = await self.db.fetch_all(query=LIST_RAW_MATERIALS)
            records = [self._schema_out(**dict(record)) for record in records]
            print(records)
            return [self._schema_out(**dict(record)) for record in records]
        except Exception as e:
            raise RawMaterialExceptions.RawMaterialListException