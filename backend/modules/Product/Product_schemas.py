from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# productos
class Product(BaseSchema):
    name: Optional[str] = None
    cost_per_bag: Optional[float] = None


class ProductInDB(Product,DateTimeModelMixin,IDModelMixin):
    name: str
    cost_per_bag: float
    created_by: UUID | str |  None
    updated_by: UUID | str |  None