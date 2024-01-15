from enum import Enum
from pydantic import UUID4, BaseModel, constr
from typing import List, Optional, Union
from uuid import UUID
from datetime import datetime
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# Definición del Enum para el estado
class BacklogState(str, Enum):
    PENDING = 'PENDING'
    ATTENDED = 'ATTENDED'


class Backlog(BaseSchema):
    id_order_product: Union[UUID, str]
    missing_amount: Optional[int] = None
    state: Optional[BacklogState] = None

class BacklogInDB(BaseSchema, DateTimeModelMixin, IDModelMixin):
    id_order_product: Union[UUID, str]
    missing_amount: int
    state: BacklogState
    created_by: Union[UUID, str, None] = None
    updated_by: Union[UUID, str, None] = None

class BacklogList(BacklogInDB):
    created_by_fullname: Optional[str] = None
    updated_by_fullname: Optional[str] = None
    product_name : str