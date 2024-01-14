from enum import Enum
from pydantic import UUID4, BaseModel, constr
from typing import List, Optional, Union
from uuid import UUID
from datetime import datetime
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# Definición del Enum para el estado
class AlertState(str, Enum):
    PENDING = 'PENDING'
    ATTENDED = 'ATTENDED'
   

class Alert(BaseSchema):
    id_factory_inventory: Union[UUID, str]
    state: Optional[AlertState] = None
    description: Optional[str] = None

class AlertInDB(BaseSchema, DateTimeModelMixin, IDModelMixin):
    id_factory_inventory: Union[UUID, str]
    state: AlertState 
    description: str
    created_by: Union[UUID, str, None] = None
    updated_by: Union[UUID, str, None] = None

class AlertList(AlertInDB):
    created_by_fullname: Optional[str] = None
    updated_by_fullname: Optional[str] = None
    factory_identifier : str
    raw_material_code :str