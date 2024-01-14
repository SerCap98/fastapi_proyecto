from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# formulas
class Formula(BaseSchema):
    raw_material_code: str
    product_name: str
    quantity: Optional[float] = None


class FormulaInDB(BaseSchema,DateTimeModelMixin,IDModelMixin):
    id_raw_material: UUID
    id_product: UUID
    quantity: float
    created_by: UUID | str |  None
    updated_by: UUID | str |  None

class FormulaList(BaseSchema,DateTimeModelMixin,IDModelMixin):
    raw_material_code: str
    product_name: str
    quantity: float
    created_by: UUID | str |  None
    created_by_fullname:str |  None
    updated_by: UUID | str |  None
    updated_by_fullname:str |  None

