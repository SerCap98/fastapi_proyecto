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
            "quantity":ManufacturedProduct.quantity if ManufacturedProduct.quantity else None,
            "created_by": current_user.id,
            "created_at": current_time
            }

        try:
            record = await self.db.fetch_one(query=CREATE_MANUFACTURED_PRODUCT , values=values)

        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductException(e)

        result = record_to_dict(record)
        return self._schema_out(**result)

    #GET BY ID PRODUCT
    async def get_manufactured_product_by_id_product(self,id_product:UUID) -> ManufacturedProductInDB:
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import GET_MANUFACTURED_PRODUCT_BY_ID_PRODUCT
        values = {
            "id_product": id_product ,
            }

        record = await self.db.fetch_one(query=GET_MANUFACTURED_PRODUCT_BY_ID_PRODUCT, values=values)
        if not record:
            raise ManufacturedProductExceptions.ManufacturedProductNotFoundException()
        return self._schema_out(**dict(record))

    #GET BY LOT NUMBER
    async def get_manufactured_product_by_lot_number(self,lot_number:str) -> ManufacturedProductInDB:
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import GET_MANUFACTURED_PRODUCT_BY_LOT_NUMBER
        values = {
            "lot_number": lot_number ,
            }

        record = await self.db.fetch_one(query=GET_MANUFACTURED_PRODUCT_BY_LOT_NUMBER, values=values)
        if not record:
            raise ManufacturedProductExceptions.ManufacturedProductNotFoundException()
        return self._schema_out(**dict(record))

    #UPDATE BY ID PRODUCT
    async def update_quantity_by_id_product(self, current_user: UserInDB, id_product:UUID, new_quantity:float) -> ManufacturedProductInDB:
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import UPDATE_QUANTITY_BY_ID_PRODUCT
        current_time = datetime.now()
        try:
            values = {
                "id_product": id_product ,
                "quantity":new_quantity,
                "updated_by": current_user.id,
                "updated_at": current_time
                }

            record = await self.db.fetch_one(query=UPDATE_QUANTITY_BY_ID_PRODUCT , values=values)
        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductException(e)
        return self._schema_out(**dict(record))

    #UPDATE BY LOT NUMBER
    async def update_quantity_by_lot_number(self, current_user: UserInDB, lot_number: str, new_quantity:float) -> ManufacturedProductInDB:
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import UPDATE_QUANTITY_BY_LOT_NUMBER
        current_time = datetime.now()
        try:
            values = {
                "lot_number":lot_number,
                "quantity":new_quantity,
                "updated_by": current_user.id,
                "updated_at": current_time
                }

            record = await self.db.fetch_one(query=UPDATE_QUANTITY_BY_LOT_NUMBER , values=values)
        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductException(e)
        return self._schema_out(**dict(record))

    #DELETE BY ID PRODUCT
    async def delete_manufactured_product_by_id_product(self,id_product:UUID) -> bool:
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import DELETE_MANUFACTURED_PRODUCT_BY_ID_PRODUCT
        try:
            values = {
                "id_product": id_product
                }

            record = await self.db.fetch_one(query=DELETE_MANUFACTURED_PRODUCT_BY_ID_PRODUCT, values=values)
        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductDeleteException()
        return True

    #DELETE BY LOT NUMBER
    async def delete_manufactured_product_by_lot_number(self,lot_number:str) -> bool:
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import DELETE_MANUFACTURED_PRODUCT_BY_LOT_NUMBER
        try:
            values = {
                "lot_number": lot_number
                }

            record = await self.db.fetch_one(query=DELETE_MANUFACTURED_PRODUCT_BY_LOT_NUMBER, values=values)
        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductDeleteException()
        return True

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
            print(f"Error: {e}")
            raise ManufacturedProductExceptions.ManufacturedProductListException()