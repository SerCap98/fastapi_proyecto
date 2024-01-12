from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# fábricas
class Factory(BaseSchema):
    identifier: Optional[str] = None


class FactoryInDB(Factory,DateTimeModelMixin,IDModelMixin):
    identifier: str
    created_by: UUID | str |  None
    updated_by: UUID | str |  None