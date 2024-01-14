from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import UUID4, BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# Productos Manufacturados
class ManufacturedProduct(BaseSchema):
    product_name: Optional[str] = None

class ManufacturedProductInDB(ManufacturedProduct,DateTimeModelMixin,IDModelMixin):
    id_product: UUID
    lot_number: str
    quantity: int
    created_by: UUID | str |  None
    updated_by: UUID | str |  None

class ManufacturedProductList(BaseSchema,DateTimeModelMixin,IDModelMixin):
    product_name: str
    lot_number: str
    quantity: int
    created_by: UUID | str |  None
    updated_by: UUID | str |  None