
from modules.RawMaterials.RawMaterial_exceptions import RawMaterialExceptions
from modules.RawMaterials.RawMaterial_repositories import RawMaterialRepository
from modules.RawMaterials.RawMaterial_schemas import RawMaterial
from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID

#import logging
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)
#logger.debug(f"Error: {e}")

class RawMaterialService:
    
    def __init__(self, db: Database):
        self.db = db

    async def create_raw_material(self, raw_material: RawMaterial) -> ServiceResult:
        raw_material_repo = RawMaterialRepository(self.db)
        try:
            new_raw_material = await raw_material_repo.create_raw_material(raw_material)
            return ServiceResult(new_raw_material)
        except Exception as e:
            return ServiceResult(e)

    async def get_raw_material_by_code(self, code: str) -> ServiceResult:
        try:
            raw_material = await RawMaterialRepository(self.db).get_raw_material_by_code(code)
            return ServiceResult(raw_material)
        except Exception  as e:
            return ServiceResult(e)


    async def update_raw_material_by_code(self, code: str, raw_material_update: RawMaterial) -> ServiceResult:
        try:
            exist=await self.get_raw_material_by_code(code)
            if not exist.success:return exist
            updated_raw_material = await RawMaterialRepository(self.db).update_raw_material_by_code(code, raw_material_update)
            return ServiceResult(updated_raw_material)
        except Exception as e:
            return ServiceResult(e)


    async def delete_raw_material_by_code(self, code: str) -> ServiceResult:
        try:
     
            exist=await self.get_raw_material_by_code(code)
            if not exist.success:return exist

            await RawMaterialRepository(self.db).delete_raw_material_by_code(code)
            return ServiceResult({"message": "Materia prima eliminada exitosamente"})
        except Exception as e:
            return ServiceResult(e)
 
    async def get_all_raw_materials(self) -> ServiceResult:
        try:
            raw_materials = await RawMaterialRepository(self.db).get_all_raw_materials()
            return ServiceResult(raw_materials)
        except Exception as e:
            return ServiceResult(e)