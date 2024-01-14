from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# productos
class FactoryRawMaterialInventory(BaseSchema):
    factory_identifier: str
    raw_material_code: str
    min_quantity: Optional[float] = None
    quantity: Optional[float] = None


class FactoryRawMaterialInventoryInDB(BaseSchema,DateTimeModelMixin,IDModelMixin):
    id_factory: UUID
    id_raw_material: UUID
    min_quantity: float
    quantity: float
    created_by: UUID | str |  None
    updated_by: UUID | str |  None

class FactoryRawMaterialInventoryList(BaseSchema,DateTimeModelMixin,IDModelMixin):
    factory_identifier: str  
    raw_material_code: str     
    min_quantity: float
    quantity: float
    created_by: UUID | str |  None
    created_by_fullname:str |  None
    updated_by: UUID | str |  None
    updated_by_fullname:str |  None

