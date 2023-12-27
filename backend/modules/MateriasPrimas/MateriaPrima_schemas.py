from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# Materias Primas
class MateriaPrima(BaseSchema):
    nombre: str | None
    cantidad: float | None
    unidad_medida: str | None


class MateriaPrimaInDB(MateriaPrima,DateTimeModelMixin,IDModelMixin):
    nombre: str
    cantidad: float
    unidad_medida: str

