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

    async def create_order_product(self, OrderProduct: OrderProduct,current_user: UserInDB,product:UUID) -> OrderProductInDB:

        from modules.OrderProduct.OrderProduct_sqlstaments import CREATE_ORDER_PRODUCT

        OrderProduct_id = str(uuid.uuid4())
        current_time = datetime.now()

        values  = {
            "id": OrderProduct_id ,
            "product": product,
            "client":OrderProduct.client.upper() if OrderProduct.client else None,
            "total_cost":OrderProduct.total_cost if OrderProduct.total_cost else None,
            "quantity":OrderProduct.quantity if OrderProduct.quantity else None,
            "note":OrderProduct.note.upper() if OrderProduct.note else None,
            "discount":OrderProduct.discount if OrderProduct.discount else None,
            "delivered":OrderProduct.delivered if OrderProduct.delivered else None,
            "date_delivered":OrderProduct.date_delivered if OrderProduct.date_delivered else None,
            "created_by": current_user.id,
            "created_at": current_time
             }

        try:
            record = await self.db.fetch_one(query=CREATE_ORDER_PRODUCT , values=values)

        except Exception as e:
            raise OrderProductExceptions.OrderProductInvalidCreateParamsException(e)

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_order_by_product(self ,product:UUID) -> OrderProductInDB:
        from modules.OrderProduct.OrderProduct_sqlstaments import GET_ORDER_PRODUCT_BY_NAME
        values = {
            "product": product
            }

        record = await self.db.fetch_one(query=GET_ORDER_PRODUCT_BY_NAME, values=values)
        if not record:
            raise OrderProductExceptions.OrderProductNotFoundException()
        return self._schema_out(**dict(record))

    async def get_all_order_product(self,
        search: str | None,
        order: str | None,
        direction: str | None
        ) -> List:
        from modules.OrderProduct.OrderProduct_sqlstaments import LIST_ORDER_PRODUCT,ORDER_PRODUCT_COMPLEMENTS,ORDER_PRODUCT_SEARCH

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = ORDER_PRODUCT_COMPLEMENTS(order, direction)
        sql_search = ORDER_PRODUCT_SEARCH()
        if not search:
            sql_sentence = LIST_ORDER_PRODUCT + sql_sentence
        else:
            sql_sentence = LIST_ORDER_PRODUCT + sql_search + sql_sentence
            values["search"] = "%" + search + "%"
        try:

            records = await self.db.fetch_all(query=sql_sentence,values=values)
            if len(records) == 0 or not records:
                return []

            return [OrderProductList(**dict(record)) for record in records]

        except Exception as e:
            raise OrderProductExceptions.ManufacturedProductListException()
