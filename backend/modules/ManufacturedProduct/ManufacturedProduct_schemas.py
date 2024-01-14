from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import UUID4, BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# Productos Manufacturados
class ManufacturedProduct(BaseSchema):
    product_name: Optional[str] = None

<<<<<<< HEAD
class ManufacturedProductInDB(ManufacturedProduct,DateTimeModelMixin,IDModelMixin):
=======


class ManufacturedProductInDB(BaseSchema,DateTimeModelMixin,IDModelMixin):
>>>>>>> b4e9e8a27de17661c1d2c9cfd107e69a3cf4c9e3
    id_product: UUID
    lot_number: str
    quantity: int
    created_by: UUID | str |  None
    updated_by: UUID | str |  None

class ManufacturedProductList(ManufacturedProduct,DateTimeModelMixin,IDModelMixin):
    product_name: str
    lot_number: str
    quantity: int
    created_by: UUID | str |  None
    created_by_fullname: str |  None
    updated_by: UUID | str |  None
    updated_by_fullname: str |  None