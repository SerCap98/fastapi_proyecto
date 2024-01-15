from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository

from modules.OrderProduct.OrderProduct_exceptions import OrderProductExceptions
from modules.OrderProduct.OrderProduct_schemas import OrderProduct,OrderProductInDB,OrderProductList


class OrderProductRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[OrderProduct]:
        return OrderProduct

    @property
    def _schema_out(self) -> Type[OrderProduct]:
        return OrderProduct

    async def create_order_product(self, OrderProduct: OrderProduct,current_user: UserInDB,product:UUID,cost:float) -> OrderProductInDB:

        from modules.OrderProduct.OrderProduct_sqlstaments import CREATE_ORDER_PRODUCT

        OrderProduct_id = str(uuid.uuid4())
        current_time = datetime.now()
        
        values  = {
            "id": OrderProduct_id ,
            "product": product,
            "client":OrderProduct.client.upper() if OrderProduct.client else None,
            "total_cost":cost*OrderProduct.quantity,
            "quantity":OrderProduct.quantity,
            "note":OrderProduct.note ,
            "discount":None,
            "delivered":False,
            "date_delivered": None,
            "created_by": current_user.id,
            "created_at": current_time
             }
      
        try:
            print(values)
            record = await self.db.fetch_one(query=CREATE_ORDER_PRODUCT , values=values)

        except Exception as e:
            raise OrderProductExceptions.OrderProductInvalidCreateParamsException(e)

        result = record_to_dict(record)
        return self._schema_out(**result)

