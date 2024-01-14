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

#import logging
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)

class ManufacturedProductRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[ManufacturedProduct]:
        return ManufacturedProduct

    @property
    def _schema_out(self) -> Type[ManufacturedProductInDB]:
        return ManufacturedProductInDB

    async def create_manufactured_product(self, ManufacturedProduct: ManufacturedProduct,current_user: UserInDB, id_product:UUID) -> ManufacturedProductInDB:

        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import CREATE_MANUFACTURED_PRODUCT

        ManufacturedProduct_id = str(uuid.uuid4())
        current_time = datetime.now()

        values = {
            "id": ManufacturedProduct_id ,
            "id_product": id_product ,
            "lot_number": ManufacturedProduct.lot_number if ManufacturedProduct.lot_number else None,
            "quantity":40,
            "created_by": current_user.id,
            "created_at": current_time
            }

        try:
            print(values["id"])
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

            print([ManufacturedProductList(**dict(record)) for record in records])

            return [ManufacturedProductList(**dict(record)) for record in records]

        except Exception as e:
            print(f"Error: {e}")
            raise ManufacturedProductExceptions.ManufacturedProductException()

    async def get_manufactured_product_by_id(self, id:UUID) -> ManufacturedProductInDB:
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import GET_MANUFACTURED_PRODUCT_BY_ID
        values = { "id": id }

        record = await self.db.fetch_one(query=GET_MANUFACTURED_PRODUCT_BY_ID, values=values)
        if not record:
            raise ManufacturedProductExceptions.ManufacturedProductNotFoundException()
        return self._schema_out(**dict(record))

    async def update_manufactured_product_by_id(self, current_user: UserInDB, id: UUID, new_product_name:str) -> ManufacturedProductInDB:
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import UPDATE_MANUFACTURED_PRODUCT_BY_ID
        current_time = datetime.now()
        try:
            values = {
                "id":id,
                "product_name":new_product_name,
                "updated_by": current_user.id,
                "updated_at": current_time
                }

            record = await self.db.fetch_one(query=UPDATE_MANUFACTURED_PRODUCT_BY_ID , values=values)
        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductException(e)
        return self._schema_out(**dict(record))

    async def delete_manufactured_product_by_id(self, id:UUID) -> bool:
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import DELETE_MANUFACTURED_PRODUCT_BY_ID
        try:
            values = {"id": id }

            record = await self.db.fetch_one(query=DELETE_MANUFACTURED_PRODUCT_BY_ID, values=values)
        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductDeleteException()
        return True
