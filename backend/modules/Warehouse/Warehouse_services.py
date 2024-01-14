
from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB
from modules.Warehouse.Warehouse_exceptions import WarehouseExceptions
from modules.Warehouse.Warehouse_repositories import WarehouseRepository
from modules.Warehouse.Warehouse_schemas import Warehouse, WarehouseInDB, WarehouseList
from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID


class WarehouseService:

    def __init__(self, db: Database):
        self.db = db

    async def create_warehouse(self, warehouse: Warehouse,current_user: UserInDB) -> ServiceResult:
        warehouse_repo = WarehouseRepository(self.db)
        try:
            new_warehouse = await warehouse_repo.create_warehouse(warehouse,current_user)
            return ServiceResult(new_warehouse)
        
        except Exception as e:
            return ServiceResult(e)

    async def get_warehouse_by_name(self, name: str) -> ServiceResult:
        try:
            warehouse = await WarehouseRepository(self.db).get_warehouse_by_name(name)
            return ServiceResult(warehouse)
        except Exception  as e:

            return ServiceResult(e)

    async def update_warehouse_by_name(self, name: str, warehouse_update: Warehouse,current_user: UserInDB) -> ServiceResult:
        try:
            exist_warehouse=await self.get_warehouse_by_name(name)
            if not exist_warehouse.success:return exist_warehouse
            updated_warehouse = await WarehouseRepository(self.db).update_warehouse_by_name(exist_warehouse, warehouse_update,current_user)
            return ServiceResult(updated_warehouse)
        except Exception as e:
            return ServiceResult(e)

    async def delete_warehouse_by_name(self, name: str) -> ServiceResult:
        try:

            exist=await self.get_warehouse_by_name(name)
            if not exist.success:return exist

            await WarehouseRepository(self.db).delete_warehouse_by_name(name)
            return ServiceResult({"message": "Almacén eliminado exitosamente"})
        except Exception as e:
            return ServiceResult(e)

    async def get_all_warehouse(self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        try:

            warehouse = await WarehouseRepository(self.db).get_all_warehouse(search,order,direction)
            warehouse_list = [WarehouseList(**item.dict()) for item in warehouse]
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=warehouse_list,
                route=f"{API_PREFIX}/warehouse",
            )
            return ServiceResult(response)
        except Exception as e:

            return ServiceResult(e)