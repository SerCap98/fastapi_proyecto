from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# Materias Primas
class MateriaPrima(BaseSchema):
    nombre: Optional[str] = None
    codigo: Optional[str] = None


class MateriaPrimaInDB(MateriaPrima,DateTimeModelMixin,IDModelMixin):
    nombre: str
    codigo: str

