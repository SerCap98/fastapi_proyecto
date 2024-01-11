from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# Materias Primas
class RawMaterial(BaseSchema):
    name: Optional[str] = None
    code: Optional[str] = None


class RawMaterialInDB(RawMaterial,DateTimeModelMixin,IDModelMixin):
    name: str
    code: str
    created_by: UUID | str | None
    updated_by: UUID | str | None

