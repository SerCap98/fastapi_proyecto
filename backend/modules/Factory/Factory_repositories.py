
from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB

from modules.Factory.Factory_exceptions import FactoryExceptions
from modules.Factory.Factory_schemas import Factory,FactoryInDB, FactoryList
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository



class FactoryRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[Factory]:
        return Factory

    @property
    def _schema_out(self) -> Type[FactoryInDB]:
        return FactoryInDB

    async def create_factory(self, factory: Factory,current_user: UserInDB) -> FactoryInDB:
        from modules.Factory.Factory_sqlstaments import CREATE_FACTORY

        factory_id = str(uuid.uuid4())
        current_time = datetime.now()
        print(factory_id)

        values = {
            "id": factory_id ,
            "identifier": factory.identifier.upper() if factory.identifier else None,
            "created_by": current_user.id,
            "created_at": current_time
            }
        print(values)
        try:
            print(values)
            record = await self.db.fetch_one(query=CREATE_FACTORY, values=values)
        except Exception as e:
            raise FactoryExceptions.FactoryInvalidCreateParamsException(e=e)

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_factory_by_identifier(self, identifier: str) -> FactoryInDB:
        from modules.Factory.Factory_sqlstaments import GET_FACTORY_BY_IDENTIFIER
        values = {"identifier": identifier.upper()}
        record = await self.db.fetch_one(query=GET_FACTORY_BY_IDENTIFIER, values=values)
        if not record:
            raise FactoryExceptions.FactoryNotFoundException()
        return self._schema_out(**dict(record))

    async def update_factory_by_identifier(self, exist_factory: ServiceResult, factory_update: Factory,current_user: UserInDB) -> FactoryInDB:
        from modules.Factory.Factory_sqlstaments import UPDATE_FACTORY_BY_IDENTIFIER

        updated_values = {
            "identifier": factory_update.identifier.upper() if factory_update.identifier else exist_factory.value.identifier,
            "updated_by": current_user.id,
            "updated_at": datetime.now()
        }
        try:
            record = await self.db.fetch_one(query=UPDATE_FACTORY_BY_IDENTIFIER, values={**updated_values, "original_identifier": exist_factory.value.identifier.upper()})

            return self._schema_out(**dict(record))
        except Exception as e:
            raise FactoryExceptions.FactoryInvalidUpdateParamsException(e=e)

    async def delete_factory_by_identifier(self, identifier: str):
        from modules.Factory.Factory_sqlstaments import DELETE_FACTORY_BY_IDENTIFIER
        try:
            await self.db.execute(query=DELETE_FACTORY_BY_IDENTIFIER, values={"identifier": identifier.upper()})
        except Exception as e:
            raise FactoryExceptions.FactoryDeletionException()
        return True

    async def get_all_factory(self,
        search: str | None,
        order: str | None,
        direction: str | None
        ) -> List:

        from modules.Factory.Factory_sqlstaments import LIST_FACTORY,FACTORY_COMPLEMENTS,FACTORY_SEARCH

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = FACTORY_COMPLEMENTS(order, direction)
        sql_search = FACTORY_SEARCH()
        if not search:
            sql_sentence = LIST_FACTORY + sql_sentence
        else:
            sql_sentence = LIST_FACTORY + sql_search + sql_sentence
            values["search"] = "%" + search + "%"
        try:

            records = await self.db.fetch_all(query=sql_sentence,values=values)
            if len(records) == 0 or not records:
                return []

            return [FactoryList(**dict(record)) for record in records]

        except Exception as e:
            raise FactoryExceptions.FactoryListException