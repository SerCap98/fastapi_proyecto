
from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB


from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID
import uuid

from modules.RawMaterials.RawMaterial_services import RawMaterialService
from modules.Factory.Factory_services import FactoryService
from modules.RawMaterialOrder.RawMaterialOrder_exceptions import RawMaterialOrderExceptions
from modules.RawMaterialOrder.RawMaterialOrder_schemas import RawMaterialOrder,RawMaterialOrderInDB,RawMaterialOrderList
from modules.RawMaterialOrder.RawMaterialOrder_repositories import RawMaterialOrderRepository

class RawMaterialOrderService:

    def __init__(self, db: Database):
        self.db = db

    async def create_raw_material_order(self, RawMaterialOrder: RawMaterialOrder,current_user: UserInDB) -> ServiceResult:
        RawMaterialOrder_repo = RawMaterialOrderRepository(self.db)

        try:

            exist_factory_and_raw_material=await self.exist_Factory_RawMaterial(RawMaterialOrder.factory_identifier,RawMaterialOrder.raw_material_code)
            if not exist_factory_and_raw_material.success:
                return exist_factory_and_raw_material

            raw_material_id=uuid.UUID(str(exist_factory_and_raw_material.value["raw_material_id"]))
            factory_id=uuid.UUID(str(exist_factory_and_raw_material.value["factory_id"]))

            new_RawMaterialOrder = await RawMaterialOrder_repo.create_raw_material_order(RawMaterialOrder,current_user, factory_id,raw_material_id)
            return ServiceResult(new_RawMaterialOrder)

        except Exception as e:
            return ServiceResult(e)

    async def get_all_order(self,
            search: str | None,
            page_num: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: str = None,
        ) -> ServiceResult:
            try:

                RawMaterialOrder = await RawMaterialOrderRepository(self.db).get_all_order(search,order,direction)
                RawMaterialOrder_list = [RawMaterialOrderList(**item.dict()) for item in RawMaterialOrder]
                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=RawMaterialOrder_list,
                    route=f"{API_PREFIX}/RawMaterialOrder",
                )
                return ServiceResult(response)
            except Exception as e:

                return ServiceResult(e)

    async def get_order_by_Factory_and_material(self, factory_identifier: str, raw_material_code: str) -> ServiceResult:
        try:

            exist_factory_and_raw_material=await self.exist_Factory_RawMaterial(factory_identifier,raw_material_code)
            if not exist_factory_and_raw_material.success:
                return exist_factory_and_raw_material
            
            raw_material_id=uuid.UUID(str(exist_factory_and_raw_material.value["raw_material_id"]))
            factory_id=uuid.UUID(str(exist_factory_and_raw_material.value["factory_id"]))

            RawMaterialOrder = await RawMaterialOrderRepository(self.db).get_order_by_Factory_and_material(raw_material_id,factory_id)
            return ServiceResult(RawMaterialOrder)
        except Exception  as e:

            return ServiceResult(e)

    async def increase_quantity_by_factory_and_material(self,current_user: UserInDB,factory_identifier: str, raw_material_code: str,increase_quantity:float) -> ServiceResult:
        try:

            exist_factory_and_raw_material=await self.exist_Factory_RawMaterial(factory_identifier,raw_material_code)
            if not exist_factory_and_raw_material.success:
                return exist_factory_and_raw_material

            raw_material_id=uuid.UUID(str(exist_factory_and_raw_material.value["raw_material_id"]))
            factory_id=uuid.UUID(str(exist_factory_and_raw_material.value["factory_id"]))

            RawMaterialOrder = await RawMaterialOrderRepository(self.db).increase_quantity_by_factory_and_material(current_user,raw_material_id,factory_id,increase_quantity)
            return ServiceResult(RawMaterialOrder)
        except Exception  as e:
            return ServiceResult(e)

    async def decrease_quantity_by_factory_and_material(self,current_user: UserInDB,factory_identifier: str, raw_material_code: str,decrease_quantity:float) -> ServiceResult:
        try:

            exist_factory_and_raw_material=await self.exist_Factory_RawMaterial(factory_identifier,raw_material_code)
            if not exist_factory_and_raw_material.success:
                return exist_factory_and_raw_material

            raw_material_id=uuid.UUID(str(exist_factory_and_raw_material.value["raw_material_id"]))
            factory_id=uuid.UUID(str(exist_factory_and_raw_material.value["factory_id"]))

            RawMaterialOrder = await RawMaterialOrderRepository(self.db).decrease_quantity_by_factory_and_material(current_user,raw_material_id,factory_id,decrease_quantity)
            return ServiceResult(RawMaterialOrder)
        except Exception  as e:
            return ServiceResult(e)

    async def delete_order_by_Factory_and_RawMaterial(self, factory_identifier: str, raw_material_code: str) -> ServiceResult:
        try:

            exist_factory_and_raw_material=await self.exist_Factory_RawMaterial(factory_identifier,raw_material_code)
            if not exist_factory_and_raw_material.success:
                return exist_factory_and_raw_material

            raw_material_id=uuid.UUID(str(exist_factory_and_raw_material.value["raw_material_id"]))
            factory_id=uuid.UUID(str(exist_factory_and_raw_material.value["factory_id"]))

            await RawMaterialOrderRepository(self.db).delete_order_by_Factory_and_RawMaterial(raw_material_id,factory_id)
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
