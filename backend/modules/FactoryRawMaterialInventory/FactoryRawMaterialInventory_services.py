
from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB


from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID
import uuid

from modules.RawMaterials.RawMaterial_services import RawMaterialService
from modules.Factory.Factory_services import FactoryService
from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_exceptions import FactoryRawMaterialInventoryExceptions
from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_schemas import FactoryRawMaterialInventory,FactoryRawMaterialInventoryInDB,FactoryRawMaterialInventoryList
from modules.FactoryRawMaterialInventory.FactoryRawMaterialInventory_repositories import FactoryRawMaterialInventoryRepository

class FactoryRawMaterialInventoryService:
    
    def __init__(self, db: Database):
        self.db = db

    async def create_Factory_RawMaterial_Inventory(self, FactRawMatlInv: FactoryRawMaterialInventory,current_user: UserInDB) -> ServiceResult:
        Factory_RawMaterial_Inventory_repo = FactoryRawMaterialInventoryRepository(self.db)


        try:
           
            exist_factory_and_raw_material=await self.exist_Factory_RawMaterial(FactRawMatlInv.factory_identifier,FactRawMatlInv.raw_material_code)
            if not exist_factory_and_raw_material.success:
                return exist_factory_and_raw_material
            
            raw_material_id=uuid.UUID(str(exist_factory_and_raw_material.value["raw_material_id"]))
            factory_id=uuid.UUID(str(exist_factory_and_raw_material.value["factory_id"]))

            new_FactRawMatlInv = await Factory_RawMaterial_Inventory_repo.create_Factory_RawMaterial_Inventory(FactRawMatlInv,
                                                                                                               current_user,
                                                                                                               raw_material_id,
                                                                                                               factory_id)
            return ServiceResult(new_FactRawMatlInv)
        
        except Exception as e:
            return ServiceResult(e)
        
    async def get_inventory_by_factory_and_material(self, factory_identifier: str, raw_material_code: str) -> ServiceResult:
        try:

            exist_factory_and_raw_material=await self.exist_Factory_RawMaterial(factory_identifier,raw_material_code)
            if not exist_factory_and_raw_material.success:
                return exist_factory_and_raw_material
            
            raw_material_id=uuid.UUID(str(exist_factory_and_raw_material.value["raw_material_id"]))
            factory_id=uuid.UUID(str(exist_factory_and_raw_material.value["factory_id"]))

            inventory = await FactoryRawMaterialInventoryRepository(self.db).get_inventory_by_Factory_and_RawMaterial(raw_material_id,factory_id)
            return ServiceResult(inventory)
        except Exception  as e:

            return ServiceResult(e)
        
    async def increase_quantity_by_factory_and_material(self,current_user: UserInDB,factory_identifier: str, raw_material_code: str,increase_quantity:float) -> ServiceResult:
        try:

            exist_factory_and_raw_material=await self.exist_Factory_RawMaterial(factory_identifier,raw_material_code)
            if not exist_factory_and_raw_material.success:
                return exist_factory_and_raw_material
            
            raw_material_id=uuid.UUID(str(exist_factory_and_raw_material.value["raw_material_id"]))
            factory_id=uuid.UUID(str(exist_factory_and_raw_material.value["factory_id"]))

            inventory = await FactoryRawMaterialInventoryRepository(self.db).increase_quantity_by_factory_and_material(current_user,raw_material_id,factory_id,increase_quantity)
            return ServiceResult(inventory)
        except Exception  as e:
            return ServiceResult(e)
        
    async def decrease_quantity_by_factory_and_material(self,current_user: UserInDB,factory_identifier: str, raw_material_code: str,decrease_quantity:float) -> ServiceResult:
        try:

            exist_factory_and_raw_material=await self.exist_Factory_RawMaterial(factory_identifier,raw_material_code)
            if not exist_factory_and_raw_material.success:
                return exist_factory_and_raw_material
            
            raw_material_id=uuid.UUID(str(exist_factory_and_raw_material.value["raw_material_id"]))
            factory_id=uuid.UUID(str(exist_factory_and_raw_material.value["factory_id"]))

            inventory = await FactoryRawMaterialInventoryRepository(self.db).decrease_quantity_by_factory_and_material(current_user,raw_material_id,factory_id,decrease_quantity)
            return ServiceResult(inventory)
        except Exception  as e:
            return ServiceResult(e)
        
    async def update_min_quantity_by_factory_and_material(self,current_user: UserInDB,factory_identifier: str, raw_material_code: str,update_min_quantity:float) -> ServiceResult:
        try:

            exist_factory_and_raw_material=await self.exist_Factory_RawMaterial(factory_identifier,raw_material_code)
            if not exist_factory_and_raw_material.success:
                return exist_factory_and_raw_material
            
            raw_material_id=uuid.UUID(str(exist_factory_and_raw_material.value["raw_material_id"]))
            factory_id=uuid.UUID(str(exist_factory_and_raw_material.value["factory_id"]))

            inventory = await FactoryRawMaterialInventoryRepository(self.db).update_min_quantity_by_factory_and_material(current_user,raw_material_id,factory_id,update_min_quantity)
            return ServiceResult(inventory)
        except Exception  as e:
            return ServiceResult(e)

    async def delete_inventory_by_factory_and_material(self, factory_identifier: str, raw_material_code: str) -> ServiceResult:
        try:

            exist_factory_and_raw_material=await self.exist_Factory_RawMaterial(factory_identifier,raw_material_code)
            if not exist_factory_and_raw_material.success:
                return exist_factory_and_raw_material
            
            raw_material_id=uuid.UUID(str(exist_factory_and_raw_material.value["raw_material_id"]))
            factory_id=uuid.UUID(str(exist_factory_and_raw_material.value["factory_id"]))

            await FactoryRawMaterialInventoryRepository(self.db).delete_inventory_by_Factory_and_RawMaterial(raw_material_id,factory_id)
            return ServiceResult({"message": "Record deleted successfully"})
        except Exception  as e:

            return ServiceResult(e)

    async def exist_Factory_RawMaterial(self, factory_identifier: str, raw_material_code: str) -> ServiceResult:
        Raw_Material_services=RawMaterialService(self.db)
        Factory_services=FactoryService(self.db)

        try:           
            exist_raw_material=await Raw_Material_services.get_raw_material_by_code(raw_material_code.upper())
            if not exist_raw_material.success:return exist_raw_material

            exist_factory=await Factory_services.get_factory_by_identifier(factory_identifier.upper())
            if not exist_factory.success:return exist_factory

            result = {
                    "raw_material_id": exist_raw_material.value.id,
                    "factory_id": exist_factory.value.id
                }

            return ServiceResult(result)
        
        except Exception as e:
            return ServiceResult(e)

    async def get_all_inventory(self, 
            search: str | None,
            page_num: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: str = None,
        ) -> ServiceResult:
            try:
                
                inventory = await FactoryRawMaterialInventoryRepository(self.db).get_all_inventory(search,order,direction)
                inventory_list = [FactoryRawMaterialInventoryList(**item.dict()) for item in inventory]
                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=inventory_list,
                    route=f"{API_PREFIX}/inventory",
                )
                return ServiceResult(response)
            except Exception as e:
                

                return ServiceResult(e)
            
    async def get_inventory_by_mat_code(self,
            code: str,
            page_num: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: str = None,
        ) -> ServiceResult:
            try:
                manufactured_product = await FactoryRawMaterialInventoryRepository(self.db).get_inventory_by_mat_code(code, order, direction)
                manufactured_product_list = [FactoryRawMaterialInventoryList(**item.dict()) for item in manufactured_product]
                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=manufactured_product_list,
                    route=f"{API_PREFIX}/manufactured-products/by-identifier/{code}",
                )
                return ServiceResult(response)
            except Exception as e:
                return ServiceResult(e)
            
    async def get_inventory_by_fact_identifier(self,
            identifier: str,
            page_num: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: str = None,
        ) -> ServiceResult:
            try:
                manufactured_product = await FactoryRawMaterialInventoryRepository(self.db).get_inventory_by_fact_identifier(identifier, order, direction)
                manufactured_product_list = [FactoryRawMaterialInventoryList(**item.dict()) for item in manufactured_product]
                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=manufactured_product_list,
                    route=f"{API_PREFIX}/manufactured-products/by-identifier/{identifier}",
                )
                return ServiceResult(response)
            except Exception as e:
                return ServiceResult(e)