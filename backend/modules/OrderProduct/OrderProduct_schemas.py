from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import UUID4, BaseModel, constr
from shared.utils.schemas_base import BaseSchema, DateTimeModelMixin, IDModelMixin

# Productos Manufacturados
class OrderProduct(BaseSchema):
    product_name: Optional[str] = None
    client: Optional[str] = None
    total_cost: Optional[float] = None
    quantity: Optional[int] = None
    note: Optional[str] = None
    discount: Optional[int] = None
    delivered: Optional[bool] = None
    date_delivered: Optional[date] = None

class OrderProductInDB(BaseSchema,DateTimeModelMixin,IDModelMixin):
    id_product: UUID
    client: str
    total_cost: float
    quantity: int
    note: str
    discount: int
    delivered: bool
    date_delivered: date
    created_by: UUID | str |  None
    updated_by: UUID | str |  None

class OrderProductList(OrderProduct,DateTimeModelMixin,IDModelMixin):
    product_name: str
    client: str
    total_cost: float
    quantity: int
    note: str
    discount: int
    delivered: bool
    date_delivered: date
    created_by: UUID | str |  None
    created_by_fullname: str |  None
    updated_by: UUID | str |  None
    updated_by_fullname: str |  None