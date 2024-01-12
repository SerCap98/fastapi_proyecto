
from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid

from modules.Factory.Factory_exceptions import FactoryExceptions
from modules.Factory.Factory_schemas import Factory,FactoryInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository


class FactoryRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[Factory]:
        return Factory

    @property
    def _schema_out(self) -> Type[FactoryInDB]:
        return FactoryInDB

    async def create_factory(self, factory: Factory) -> FactoryInDB:
        from backend.modules.Factory.Factory_sqlstaments import CREATE_FACTORY

        factory_id = str(uuid.uuid4())
        current_time = datetime.now()
        factory.identifier = factory.identifier.upper()

        values = {
            "id": factory_id,
            "identifier": factory.identifier,
            "created_at": current_time,
            "updated_at": current_time
        }

        try:
            record = await self.db.fetch_one(query=CREATE_FACTORY, values=values)
        except Exception as e:
            raise FactoryExceptions.FactoryCreationException()

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_factory_by_identifier(self, identifier: str) -> FactoryInDB:
        from backend.modules.Factory.Factory_sqlstaments import GET_FACTORY_BY_ID
        values = {"identifier": identifier}
        record = await self.db.fetch_one(query=GET_FACTORY_BY_ID, values=values)
        if not record:
            raise FactoryExceptions.FactoryNotFoundException()
        return self._schema_out(**dict(record))

    async def update_factory_by_identifier(self, identifier: str, factory_update: Factory) -> FactoryInDB:
        from backend.modules.Factory.Factory_sqlstaments import UPDATE_FACTORY_BY_ID

        updated_values = {
            "identifier": factory_update.identifier.upper() if factory_update.identifier else None,
            "updated_at": datetime.now()
        }

        try:
            record = await self.db.fetch_one(query=UPDATE_FACTORY_BY_ID, values=updated_values)
            return self._schema_out(**dict(record))
        except Exception as e:
            raise FactoryExceptions.FactoryUpdateException()

    async def delete_factory_by_identifier(self, identifier: str):
        from backend.modules.Factory.Factory_sqlstaments import DELETE_FACTORY_BY_ID
        try:
            await self.db.execute(query=DELETE_FACTORY_BY_ID, values={"identifier": identifier.upper()})
        except Exception as e:
            raise FactoryExceptions.FactoryDeletionException()
        return True

    async def get_all_factories(self) -> List[FactoryInDB]:
        from backend.modules.Factory.Factory_sqlstaments import LIST_FACTORY

        try:
            records = await self.db.fetch_all(query=LIST_FACTORY)
            return [self._schema_out(**dict(record)) for record in records]
        except Exception as e:
            raise FactoryExceptions.FactoryListException