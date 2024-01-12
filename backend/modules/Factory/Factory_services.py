
from modules.Factory.Factory_exceptions import FactoryExceptions
from modules.Factory.Factory_repositories import FactoryRepository
from modules.Factory.Factory_schemas import Factory
from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID

#import logging
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)
#logger.debug(f"Error: {e}")

class FactoryService:
    
    def __init__(self, db: Database):
        self.db = db

    async def create_factory(self, factory: Factory) -> ServiceResult:
        factory_repo = FactoryRepository(self.db)
        try:
            new_factory = await factory_repo.create_factory(factory)
            return ServiceResult(new_factory)
        except Exception as e:
            return ServiceResult(e)

    async def get_factory_by_identifier(self, identifier: str) -> ServiceResult:
        try:
            factory = await FactoryRepository(self.db).get_factory_by_identifier(identifier)
            return ServiceResult(factory)
        except Exception  as e:
            return ServiceResult(e)


    async def update_factory_by_identifier(self, identifier: str, factory_update: Factory) -> ServiceResult:
        try:
            exist=await self.get_factory_by_identifier(identifier)
            if not exist.success:return exist
            updated_factory = await FactoryRepository(self.db).update_factory_by_identifier(identifier, factory_update)
            return ServiceResult(updated_factory)
        except Exception as e:
            return ServiceResult(e)


    async def delete_factory_by_identifier(self, identifier: str) -> ServiceResult:
        try:
     
            exist=await self.get_factory_by_identifier(identifier)
            if not exist.success:return exist

            await FactoryRepository(self.db).delete_factory_by_identifier(identifier)
            return ServiceResult({"message": "Fábrica eliminada exitosamente"})
        except Exception as e:
            return ServiceResult(e)
 
    async def get_all_factories(self) -> ServiceResult:
        try:
            factory = await FactoryRepository(self.db).get_all_factory()
            return ServiceResult(factory)
        except Exception as e:
            return ServiceResult(e)