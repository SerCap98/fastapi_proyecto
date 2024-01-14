from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# formulas
class Formula(BaseSchema):
    quantity: Optional[float] = None
    raw_material_code: str
    product_name: str


class FormulaInDB(BaseSchema,DateTimeModelMixin,IDModelMixin):
    quantity: float
    id_raw_material: UUID
    id_product: UUID
    created_by: UUID | str |  None
    updated_by: UUID | str |  None

class FormulaList(BaseSchema,DateTimeModelMixin,IDModelMixin):
    quantity: float
    raw_material_code: str
    product_name: str
    created_by: UUID | str |  None
    created_by_fullname:str |  None
    updated_by: UUID | str |  None
    updated_by_fullname:str |  None

