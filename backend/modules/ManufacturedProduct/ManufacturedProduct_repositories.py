
from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB

from modules.ManufacturedProduct.ManufacturedProduct_exceptions import ManufacturedProductExceptions
from modules.ManufacturedProduct.ManufacturedProduct_schemas import ManufacturedProduct,ManufacturedProductInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ManufacturedProductRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[ManufacturedProduct]:
        return ManufacturedProduct

    @property
    def _schema_out(self) -> Type[ManufacturedProductInDB]:
        return ManufacturedProductInDB

    async def create_manufactured_product(self, manufactured_product: ManufacturedProduct, id_product: UUID, current_user: UserInDB) -> ManufacturedProductInDB:
        product_query = "SELECT id FROM Product WHERE id = :id_product"
        product_exists = await self.db.fetch_one(query=product_query, values={"id_product": id_product})

        if not product_exists:
            raise Exception("El producto ingresado no se ha fabricado")

        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import CREATE_MANUFACTURED_PRODUCT

        manufactured_product_id = str(uuid.uuid4())
        current_time = datetime.now()
        print(manufactured_product_id)

        values = {
            "id": manufactured_product_id ,
            "id_product": id_product,
            "lot_number": manufactured_product.lot_number.upper() if manufactured_product.lot_number else None,
            "quantity": manufactured_product.quantity if manufactured_product.quantity else None,
            "created_by": current_user.id,
            "created_at": current_time
            }
        print(values)
        try:
            print(values)
            record = await self.db.fetch_one(query=CREATE_MANUFACTURED_PRODUCT, values=values)
        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductInvalidCreateParamsException(e=e)

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_manufactured_product_by_lot_number(self, lot_number: str) -> ManufacturedProductInDB:
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import GET_MANUFACTURED_PRODUCT_BY_LOT_NUMBER
        values = {"lot_number": lot_number.upper()}
        record = await self.db.fetch_one(query=GET_MANUFACTURED_PRODUCT_BY_LOT_NUMBER, values=values)
        if not record:
            raise ManufacturedProductExceptions.ManufacturedProductNotFoundException()
        return self._schema_out(**dict(record))

    async def update_manufactured_product_by_lot_number(self, exist_manufactured_product: ServiceResult, id_product: UUID, manufactured_product_update: ManufacturedProduct,current_user: UserInDB) -> ManufacturedProductInDB:
        product_query = "SELECT id FROM Product WHERE id = :id_product"
        product_exists = await self.db.fetch_one(query=product_query, values={"id_product": id_product})

        if not product_exists:
            raise Exception("El producto ingresado no se ha fabricado")

        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import UPDATE_MANUFACTURED_PRODUCT_BY_LOT_NUMBER

        updated_values = {
            "id_product": id_product,
            "lot_number": manufactured_product_update.lot_number.upper() if manufactured_product_update.lot_number else exist_manufactured_product.value.lot_number,
            "quantity": manufactured_product_update.quantity if manufactured_product_update.quantity else exist_manufactured_product.value.quantity,
            "updated_by": current_user.id,
            "updated_at": datetime.now()
        }
        try:
            record = await self.db.fetch_one(query=UPDATE_MANUFACTURED_PRODUCT_BY_LOT_NUMBER, values={**updated_values, "original_lot_number": exist_manufactured_product.value.lot_number.upper()})

            return self._schema_out(**dict(record))
        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductInvalidUpdateParamsException(e=e)

    async def delete_manufactured_product_by_lot_number(self, lot_number: str):
        from modules.ManufacturedProduct.ManufacturedProduct_sqlstaments import DELETE_MANUFACTURED_PRODUCT_BY_LOT_NUMBER
        try:
            await self.db.execute(query=DELETE_MANUFACTURED_PRODUCT_BY_LOT_NUMBER, values={"lot_number": lot_number.upper()})
        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductDeletionException()
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

            return [self._schema_out(**dict(record)) for record in records]

        except Exception as e:
            raise ManufacturedProductExceptions.ManufacturedProductListException