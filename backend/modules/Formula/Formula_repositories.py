from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository

from modules.Formula.Formula_exceptions import FormulaExceptions
from modules.Formula.Formula_schemas import Formula,FormulaInDB,FormulaList

#import logging
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)


class FormulaRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[Formula]:
        return Formula

    @property
    def _schema_out(self) -> Type[FormulaInDB]:
        return FormulaInDB

    async def create_formula(self, Form: Formula,current_user: UserInDB,raw_material:UUID ,product:UUID) -> FormulaInDB:

        from modules.Formula.Formula_sqlstaments import CREATE_FORMULA

        formula_id = str(uuid.uuid4())
        current_time = datetime.now()

        values = {
            "id": formula_id ,
            "raw_material": raw_material ,
            "product": product ,
            "quantity":Form.quantity if Form.quantity else None,
            "created_by": current_user.id,
            "created_at": current_time
            }

        try:
            record = await self.db.fetch_one(query=CREATE_FORMULA, values=values)

        except Exception as e:
            raise FormulaExceptions.FormulaException(e)

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_formula_by_Product_and_RawMaterial(self,raw_material:UUID ,product:UUID) -> FormulaInDB:
        from modules.Formula.Formula_sqlstaments import GET_PRODUCT_RAW_MATERIAL_FORMULA
        values = {
            "product": product ,
            "raw_material": raw_material
            }

        record = await self.db.fetch_one(query=GET_PRODUCT_RAW_MATERIAL_FORMULA, values=values)
        if not record:
            raise FormulaExceptions.FormulaNotFoundException()
        return self._schema_out(**dict(record))

    async def get_all_formula(self, search: str | None, order: str | None, direction: str | None ) -> List:
        from modules.Formula.Formula_sqlstaments import LIST_FORMULA,FORMULA_COMPLEMENTS,FORMULA_SEARCH

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = FORMULA_COMPLEMENTS(order, direction)
        sql_search = FORMULA_SEARCH()
        if not search:
            sql_sentence = LIST_FORMULA + sql_sentence
        else:
            sql_sentence = LIST_FORMULA + sql_search + sql_sentence
            values["search"] = "%" + search + "%"
        try:

            records = await self.db.fetch_all(query=sql_sentence,values=values)
            if len(records) == 0 or not records:
                return []
            return [FormulaList(**dict(record)) for record in records]

        except Exception as e:

            raise FormulaExceptions.InventoryListException()