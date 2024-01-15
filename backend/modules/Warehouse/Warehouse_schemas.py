from typing import List, Optional
from uuid import UUID
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

class type1(Enum):
    MAIN = "MAIN"
    CONSIGNED = "CONSIGNED"

# Warehouse
class Warehouse(BaseSchema):
    name: Optional[str] = None
    type: Optional[type1] = None
    type_num: Optional[int] = None

class WarehouseInDB(BaseSchema,DateTimeModelMixin,IDModelMixin):
    name: str
    type: type1
    type_num: int
    created_by: UUID | str |  None
    updated_by: UUID | str |  None

class WarehouseList(BaseSchema,DateTimeModelMixin,IDModelMixin):
    name: str
    type: type1
    type_num: int
    created_by: UUID | str |  None
    created_by_fullname: str |  None
    updated_by: UUID | str |  None
    updated_by_fullname: str |  None