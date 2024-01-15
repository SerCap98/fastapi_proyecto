
from datetime import datetime
from enum import Enum
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB

from modules.Backlog.Backlog_exceptions import BacklogExceptions
from modules.Backlog.Backlog_schemas import Backlog,BacklogInDB, BacklogList, BacklogState

from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository



class BacklogRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[Backlog]:
        return Backlog

    @property
    def _schema_out(self) -> Type[BacklogInDB]:
        return BacklogInDB

    async def create_backlog(self, backlog: Backlog,current_user: UserInDB) -> BacklogInDB:
        from modules.Backlog.Backlog_sqlstaments import CREATE_BACKLOG

        product_id = str(uuid.uuid4())
        current_time = datetime.now()
        try:
            values = {
                "id": product_id ,
                "id_order_product": backlog.id_order_product ,
                "missing_amount": backlog.missing_amount if backlog.missing_amount else None,
                "state": backlog.state if backlog.state else BacklogState.PENDING.value,
                "created_by": current_user.id,
                "created_at": current_time
            }

            record = await self.db.fetch_one(query=CREATE_BACKLOG, values=values)
        except Exception as e:
            print(e)
            raise BacklogExceptions.BacklogInvalidCreateParamsException(e=e)

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_backlog(self, id: UUID) -> BacklogInDB:
        from modules.Backlog.Backlog_sqlstaments import GET_BACKLOG_BY_ID
        values = {"id": id}
        record = await self.db.fetch_one(query=GET_BACKLOG_BY_ID, values=values)
        if not record:
            raise BacklogExceptions.BacklogNotFoundException()
        return self._schema_out(**dict(record))

    async def attended_backlog(self, id:UUID,current_user: UserInDB) -> BacklogInDB:
            from modules.Backlog.Backlog_sqlstaments import ATTENDED_BACKLOG_BY_ID
            current_time = datetime.now()
            updated_values = {
                "id": id,
                "state": BacklogState.ATTENDED.value,
                "updated_by": current_user.id,
                "updated_at": current_time
            }
            try:

                record = await self.db.fetch_one(query=ATTENDED_BACKLOG_BY_ID, values=updated_values)

                return self._schema_out(**dict(record))
            except Exception as e:
                print(e)
                raise BacklogExceptions.BacklogInvalidUpdateParamsException(e=e)

    async def pending_backlog(self, id:UUID,current_user: UserInDB) -> BacklogInDB:
            from modules.Backlog.Backlog_sqlstaments import ATTENDED_BACKLOG_BY_ID
            current_time = datetime.now()
            updated_values = {
                "id": id,
                "state": BacklogState.PENDING.value,
                "updated_by": current_user.id,
                "updated_at": current_time
            }
            try:
            
                record = await self.db.fetch_one(query=ATTENDED_BACKLOG_BY_ID, values=updated_values)
               
                return self._schema_out(**dict(record))
            except Exception as e:
                print(e)
                raise BacklogExceptions.BacklogInvalidUpdateParamsException(e=e)

    async def delete_backlog(self, id: UUID) -> bool:
        from modules.Backlog.Backlog_sqlstaments import DELETE_BACKLOG_BY_ID
        try:
            await self.db.execute(query=DELETE_BACKLOG_BY_ID, values={"id": id})
        except Exception as e:
            raise BacklogExceptions.BacklogDeleteException()
        return True


    async def get_all_backlog(self,
            search: str | None,
            order: str | None,
            direction: str | None
            ) -> List:
            from modules.Backlog.Backlog_sqlstaments import LIST_BACKLOG,BACKLOG_COMPLEMENTS,BACKLOG_SEARCH

            order = order.lower() if order != None else None
            direction = direction.upper() if order != None else None
            values = {}
            sql_sentence = BACKLOG_COMPLEMENTS(order, direction)
            sql_search = BACKLOG_SEARCH()
            if not search:
                sql_sentence = LIST_BACKLOG + sql_sentence
            else:
                sql_sentence = LIST_BACKLOG + sql_search + sql_sentence
                values["search"] = "%" + search + "%"
            try:

                records = await self.db.fetch_all(query=sql_sentence,values=values)
                if len(records) == 0 or not records:
                    return []

                return [BacklogList(**dict(record)) for record in records]

            except Exception as e:
              print(e)
              raise BacklogExceptions.BacklogListException(e)
