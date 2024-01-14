
from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB
from modules.RawMaterials.RawMaterial_exceptions import RawMaterialExceptions
from modules.RawMaterials.RawMaterial_repositories import RawMaterialRepository
from modules.RawMaterials.RawMaterial_schemas import RawMaterial, RawMaterialInDB, RawMaterialList
from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID


class RawMaterialService:
    
    def __init__(self, db: Database):
        self.db = db

    async def create_raw_material(self, raw_material: RawMaterial,current_user: UserInDB) -> ServiceResult:
        raw_material_repo = RawMaterialRepository(self.db)
        try:
            new_raw_material = await raw_material_repo.create_raw_material(raw_material,current_user)
            return ServiceResult(new_raw_material,)
        
        except Exception as e:
            return ServiceResult(e)

    async def get_raw_material_by_code(self, code: str) -> ServiceResult:
        try:
            raw_material = await RawMaterialRepository(self.db).get_raw_material_by_code(code)
            return ServiceResult(raw_material)
        except Exception  as e:

            return ServiceResult(e)


    async def update_raw_material_by_code(self, code: str, raw_material_update: RawMaterial,current_user: UserInDB) -> ServiceResult:
        try:
            exist_raw_material=await self.get_raw_material_by_code(code)
            if not exist_raw_material.success:return exist_raw_material
            updated_raw_material = await RawMaterialRepository(self.db).update_raw_material_by_code(exist_raw_material, raw_material_update,current_user)
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
 
    async def get_all_raw_materials(self, 
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        try:
     
            raw_materials = await RawMaterialRepository(self.db).get_all_raw_material(search,order,direction)
            raw_materials_list = [RawMaterialList(**item.dict()) for item in raw_materials]
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=raw_materials_list,
                route=f"{API_PREFIX}/raw-materials",
            )
            return ServiceResult(response)
        except Exception as e:
            
            return ServiceResult(e)