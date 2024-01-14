from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository

from modules.ManufacturedProduct.ManufacturedProduct_exceptions import ManufacturedProductExceptions
from modules.ManufacturedProduct.ManufacturedProduct_schemas import ManufacturedProduct,ManufacturedProductInDB,ManufacturedProductList


class ManufacturedProductRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[ManufacturedProduct]:
        return ManufacturedProduct

    @property
    def _schema_out(self) -> Type[ManufacturedProductInDB]:
        return ManufacturedProductInDB

    async def create_manufactured_product(self, ManufacturedProduct: ManufacturedProduct,current_user: UserInDB, product:UUID) -> ManufacturedProductInDB:

        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import CREATE_MANUFACTURED_PRODUCT

        ManufacturedProduct_id = str(uuid.uuid4())
        current_time = datetime.now()

        values = {
            "id": ManufacturedProduct_id ,
            "id_product": product ,
            "lot_number": "123-456-789",
            "quantity":40,
            "created_by": current_user.id,
            "created_at": current_time
            }

        try:
 
            record = await self.db.fetch_one(query=CREATE_MANUFACTURED_PRODUCT , values=values)

        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductException(e)

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_all_manufactured_product(self,
        search: str | None,
        order: str | None,
        direction: str | None
        ) -> List:
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import LIST_MANUFACTURED_PRODUCT,MANUFACTURED_PRODUCT_COMPLEMENTS,MANUFACTURED_PRODUCT_SEARCH

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = MANUFACTURED_PRODUCT_COMPLEMENTS(order, direction)
        sql_search = MANUFACTURED_PRODUCT_SEARCH()
        if not search:
            sql_sentence = LIST_MANUFACTURED_PRODUCT + sql_sentence
        else:
            sql_sentence = LIST_MANUFACTURED_PRODUCT + sql_search + sql_sentence
            values["search"] = "%" + search + "%"
        try:

            records = await self.db.fetch_all(query=sql_sentence,values=values)
            if len(records) == 0 or not records:
                return []


            return [ManufacturedProductList(**dict(record)) for record in records]

        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductException()
