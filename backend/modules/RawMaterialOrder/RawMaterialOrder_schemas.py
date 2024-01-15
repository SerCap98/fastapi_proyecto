from enum import Enum
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

class state1(Enum):
    APPROVED = "APPROVED"
    REFUSED = "REFUSED"

# ordenes de materia prima
class RawMaterialOrder(BaseSchema):
    raw_material_code: str
    factory_identifier: str
    quantity: Optional[float] = None
    state: state1
    note: Optional[str] = None
    cost: Optional[float] = None
    delivered: Optional[bool] = None
    date_delivered: Optional[date] = None


class RawMaterialOrderInDB(BaseSchema,DateTimeModelMixin,IDModelMixin):
    id_raw_material: UUID
    id_factory: UUID
    quantity: float
    state: state1
    note: str
    cost: float
    delivered: bool
    date_delivered: date
    created_by: UUID | str |  None
    updated_by: UUID | str |  None

class RawMaterialOrderList(BaseSchema,DateTimeModelMixin,IDModelMixin):
    raw_material_code: str
    factory_identifier: str
    quantity: float
    state: state1
    note: str
    cost: float
    delivered: bool
    date_delivered: date
    created_by: UUID | str |  None
    created_by_fullname:str |  None
    updated_by: UUID | str |  None
    updated_by_fullname:str |  None

