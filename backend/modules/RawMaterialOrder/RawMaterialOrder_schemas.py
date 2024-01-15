from enum import Enum
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

class state1(Enum):
    APPROVED = "APPROVED"
    REFUSED = "REFUSED"
    ON_HOLD = "ON HOLD"

# ordenes de materia prima
class RawMaterialOrder(BaseSchema):
    raw_material_code: str
    factory_identifier: str
    quantity: Optional[float] = None
    note: Optional[str] = None
    cost: Optional[float] = None

class RawMaterialOrderToUpdated(BaseSchema):
    quantity: Optional[float] = None
    note: Optional[str] = None
    cost: Optional[float] = None


class RawMaterialOrderInDB(BaseSchema,DateTimeModelMixin,IDModelMixin):
    id_raw_material: UUID
    id_factory: UUID
    quantity: float
    state: state1
    note: str |  None
    cost: float
    delivered: bool
    date_delivered: date |  None
    created_by: UUID | str 
    updated_by: UUID | str |  None

class RawMaterialOrderList(BaseSchema,DateTimeModelMixin,IDModelMixin):
    raw_material_code: str
    factory_identifier: str
    quantity: float
    state: state1
    note: str |  None
    cost: float
    delivered: bool
    date_delivered: date |  None
    created_by: UUID | str 
    created_by_fullname:str 
    updated_by: UUID | str |  None
    updated_by_fullname:str |  None

