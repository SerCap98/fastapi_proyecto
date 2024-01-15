from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import UUID4, BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# Productos Manufacturados
class OrderProduct(BaseSchema):
    product_name: Optional[str] = None
    client: Optional[str] = None
    quantity: Optional[int] = None
    note: Optional[str] = None

class OrderProductToUpdate(BaseSchema):
    client: Optional[str] = None
    quantity: Optional[int] = None
    note: Optional[str] = None

class OrderProductInDB(BaseSchema,DateTimeModelMixin,IDModelMixin):
    id_product: UUID
    client: str
    total_cost: float
    quantity: int
    note: str |  None
    discount: float |  None
    delivered: bool
    date_delivered: date |  None
    created_by: UUID | str |  None
    updated_by: UUID | str |  None

class OrderProductList(OrderProduct,DateTimeModelMixin,IDModelMixin):
    product_name: str
    client: str
    total_cost: float
    quantity: int
    note: str |  None
    discount: float |  None
    delivered: bool
    date_delivered: date |  None
    created_by: UUID | str |  None
    created_by_fullname: str |  None
    updated_by: UUID | str |  None
    updated_by_fullname: str |  None