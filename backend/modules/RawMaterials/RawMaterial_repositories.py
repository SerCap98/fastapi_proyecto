
from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid

from modules.RawMaterials.RawMaterial_exceptions import RawMaterialExceptions
from modules.RawMaterials.RawMaterial_schemas import RawMaterial,RawMaterialInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository


class RawMaterialRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[RawMaterial]:
        return RawMaterial

    @property
    def _schema_out(self) -> Type[RawMaterialInDB]:
        return RawMaterialInDB

    async def create_materia_prima(self, raw_material: RawMaterial) -> RawMaterialInDB:
        from backend.modules.RawMaterials.RawMaterial_sqlstaments import CREATE_RAW_MATERIAL

        raw_material_id = str(uuid.uuid4())
        current_time = datetime.now()
        raw_material.name = raw_material.name.upper()
        raw_material.code = raw_material.code.upper()

        values = {
            "id": raw_material_id,
            "name": raw_material.name,
            "code": raw_material.code,
            "created_at": current_time
        }

        try:
            record = await self.db.fetch_one(query=CREATE_RAW_MATERIAL, values=values)
        except Exception as e:
            raise RawMaterialExceptions.RawMaterialCreationException()

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_raw_material_by_code(self, code: str) -> RawMaterialInDB:
        from backend.modules.RawMaterials.RawMaterial_sqlstaments import GET_RAW_MATERIAL_BY_CODE
        values = {"code": code}
        record = await self.db.fetch_one(query=GET_RAW_MATERIAL_BY_CODE, values=values)
        if not record:
            raise RawMaterialExceptions.RawMaterialNotFoundException()
        return self._schema_out(**dict(record))

    async def update_raw_material_by_code(self, code: str, raw_material_update: RawMaterial) -> RawMaterialInDB:
        from backend.modules.RawMaterials.RawMaterial_sqlstaments import UPDATE_RAW_MATERIAL_BY_CODE

        updated_values = {
            "name": raw_material_update.nombre.upper() if raw_material_update.name else None,
            "code": code.upper(),
            "updated_at": datetime.now()
        }

        try:
            record = await self.db.fetch_one(query=UPDATE_RAW_MATERIAL_BY_CODE, values=updated_values)
            return self._schema_out(**dict(record))
        except Exception as e:
            raise RawMaterialExceptions.RawMaterialUpdateException()

    async def delete_raw_material_by_code(self, code: str):
        from backend.modules.RawMaterials.RawMaterial_sqlstaments import DELETE_RAW_MATERIAL_BY_CODE
        try:
            await self.db.execute(query=DELETE_RAW_MATERIAL_BY_CODE, values={"code": code.upper()})
        except Exception as e:
            raise RawMaterialExceptions.RawMaterialDeletionException()
        return True

    async def get_all_materias_primas(self) -> List[RawMaterialInDB]:
        from backend.modules.RawMaterials.RawMaterial_sqlstaments import LIST_RAW_MATERIALS

        try:
            records = await self.db.fetch_all(query=LIST_RAW_MATERIALS)
            return [self._schema_out(**dict(record)) for record in records]
        except Exception as e:
            raise RawMaterialExceptions.RawMaterialListException