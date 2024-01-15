
from modules.ManufacturedProduct.ManufacturedProduct_services import ManufacturedProductService
from modules.Warehouse.Warehouse_services import WarehouseService
from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB
from modules.WarehouseProductInventory.WarehouseProductInventory_exceptions import WarehouseProductInventoryExceptions
from modules.WarehouseProductInventory.WarehouseProductInventory_repositories import WarehouseProductInventoryRepository
from modules.WarehouseProductInventory.WarehouseProductInventory_schemas import WarehouseProductInventory, WarehouseProductInventoryInDB, WarehouseProductInventoryList, WarehouseProductInventoryListSummary
from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID


class WarehouseProductInventoryServices:

    def __init__(self, db: Database):
        self.db = db

    async def create_WarehouseProductInventory(self, warehouse_product_inventory: WarehouseProductInventory,current_user: UserInDB) -> ServiceResult:
        WarehouseProductInventory_repo = WarehouseProductInventoryRepository(self.db)
        try:
            if (warehouse_product_inventory.name_warehouse):
                exist_warehouse=await self.exist_warehouse(warehouse_product_inventory.name_warehouse.upper())
                if not exist_warehouse.success:return exist_warehouse
            else: return ServiceResult(WarehouseProductInventoryExceptions.WarehouseProductInventoryInvalidCreateParamsException())
            exist_manufactured_product=await self.exist_manufactured_product(warehouse_product_inventory.id_manufactured_product)
            if not exist_manufactured_product.success:return exist_manufactured_product
          
            new_WarehouseProductInventory = await WarehouseProductInventory_repo.create_WarehouseProductInventory(warehouse_product_inventory,exist_warehouse.value["warehouse_id"],current_user)
            return ServiceResult(new_WarehouseProductInventory)
        
        except Exception as e:
            return ServiceResult(e)

    async def exist_warehouse(self, warehouse_name: str) -> ServiceResult:
        warehouse_services=WarehouseService(self.db)

        try:
     
            exist_warehouse=await warehouse_services.get_warehouse_by_name(warehouse_name)
            if not exist_warehouse.success:return exist_warehouse

            result = { "warehouse_id": exist_warehouse.value.id }
  
            return ServiceResult(result)

        except Exception as e:
            return ServiceResult(e)
        
    async def exist_manufactured_product(self, manufactured_product_id: UUID) -> ServiceResult:
        manufactured_product_services=ManufacturedProductService(self.db)

        try:
            exist_manufactured_product=await manufactured_product_services.get_manufactured_product_by_id(manufactured_product_id)
            if not exist_manufactured_product.success:return exist_manufactured_product

            result = { "manufactured_product": exist_manufactured_product.value.id }

            return ServiceResult(result)

        except Exception as e:
            return ServiceResult(e)
        
    async def get_warehouse_product_inventory_by_id(self, id: UUID) -> ServiceResult:
        try:
            warehouse_product_inventory = await WarehouseProductInventoryRepository(self.db).get_warehouse_product_inventory_by_id(id)
            return ServiceResult(warehouse_product_inventory)

        except Exception  as e:
            return ServiceResult(e)
        
    async def decrease_quantity_available(self,current_user: UserInDB,id: UUID, decrease_quantity: int) -> ServiceResult:
        try:

            exist_inventory=await self.get_warehouse_product_inventory_by_id(id)
            if not exist_inventory.success:
                return exist_inventory

            inventory = await WarehouseProductInventoryRepository(self.db).decrease_quantity_available(current_user,id,decrease_quantity)
            return ServiceResult(inventory)
        except Exception  as e:
            return ServiceResult(e)
        
    async def transfer_inventory(self,current_user: UserInDB,id: UUID, new_warehouse: str) -> ServiceResult:
        try:

            exist_inventory=await self.get_warehouse_product_inventory_by_id(id)
            if not exist_inventory.success:
                return exist_inventory
           
            exist_warehouse=await self.exist_warehouse(new_warehouse.upper())
            if not exist_warehouse.success:return exist_warehouse
         

            inventory = await WarehouseProductInventoryRepository(self.db).transfer_inventory(current_user,id,exist_warehouse.value["warehouse_id"])
            return ServiceResult(inventory)
        except Exception  as e:
            return ServiceResult(e)
        
    async def delete_Inventory(self, id: UUID) -> ServiceResult:
        try:

            exist_inventory=await self.get_warehouse_product_inventory_by_id(id)
            if not exist_inventory.success:
                return exist_inventory
            

            await WarehouseProductInventoryRepository(self.db).delete_Inventory(id)
            return ServiceResult({"message": "Record deleted successfully"})
        except Exception  as e:

            return ServiceResult(e)
        
    async def get_all_inventory(self, 
            search: str | None,
            page_num: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: str = None,
        ) -> ServiceResult:
            try:
                
                inventory = await WarehouseProductInventoryRepository(self.db).get_all_inventory(search,order,direction)
                inventory_list = [WarehouseProductInventoryList(**item.dict()) for item in inventory]
                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=inventory_list,
                    route=f"{API_PREFIX}/inventory",
                )
                return ServiceResult(response)
            except Exception as e:
                

                return ServiceResult(e)
            
    async def get_all_summary_inventory(self, 
            search: str | None,
            page_num: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: str = None,
        ) -> ServiceResult:
            try:
                
                inventory = await WarehouseProductInventoryRepository(self.db).get_all_summary_inventory(search,order,direction)
                inventory_list = [WarehouseProductInventoryListSummary(**item.dict()) for item in inventory]
                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=inventory_list,
                    route=f"{API_PREFIX}/inventory-summary",
                )
                return ServiceResult(response)
            except Exception as e:
                

                return ServiceResult(e)
            