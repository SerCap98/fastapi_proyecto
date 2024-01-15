from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr
from modules.Warehouse.Warehouse_schemas import type1
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin



# Warehouse
class WarehouseProductInventory(BaseSchema):
    name_warehouse:str | None
    id_manufactured_product: UUID | str |  None
  

class WarehouseProductInventoryInDB(BaseSchema,DateTimeModelMixin,IDModelMixin):
    id_warehouse:UUID | str 
    id_manufactured_product:UUID | str 
    available_product: int
    created_by: UUID | str |  None
    updated_by: UUID | str |  None

class WarehouseProductInventoryList(BaseSchema,DateTimeModelMixin,IDModelMixin):
    id_warehouse:UUID | str 
    id_manufactured_product:UUID | str 
    available_product: int
    warehouse_name:str
    warehouse_type:type1
    product_name:str
    lot_number:str
    created_by: UUID | str |  None
    created_by_fullname: str |  None
    updated_by: UUID | str |  None
    updated_by_fullname: str |  None

class WarehouseProductInventoryListSummary(BaseSchema):
    warehouse_name:str
    product_name:str
    total_available: int
  