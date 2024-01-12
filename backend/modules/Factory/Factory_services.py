from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB
from modules.Factory.Factory_exceptions import FactoryExceptions
from modules.Factory.Factory_repositories import FactoryRepository
from modules.Factory.Factory_schemas import Factory
from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID


class FactoryService:

    def __init__(self, db: Database):
        self.db = db

    async def create_factory(self, factory: Factory,current_user: UserInDB) -> ServiceResult:
        factory_repo = FactoryRepository(self.db)
        try:
            new_factory = await factory_repo.create_factory(factory,current_user)
            return ServiceResult(new_factory,)

        except Exception as e:
            return ServiceResult(e)

    async def get_factory_by_identifier(self, identifier: str) -> ServiceResult:
        try:
            factory = await FactoryRepository(self.db).get_factory_by_identifier(identifier)
            return ServiceResult(factory)
        except Exception  as e:

            return ServiceResult(e)


    async def update_factory_by_identifier(self, identifier: str, factory_update: Factory,current_user: UserInDB) -> ServiceResult:
        try:
            exist_factory=await self.get_factory_by_identifier(identifier)
            if not exist_factory.success:return exist_factory
            updated_factory = await FactoryRepository(self.db).update_factory_by_identifier(exist_factory, factory_update,current_user)
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

    async def get_all_factory(self, 
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        try:

            factory = await FactoryRepository(self.db).get_all_factory(search,order,direction)
            factory_list = [Factory(**item.dict()) for item in factory]
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=factory_list,
                route=f"{API_PREFIX}/factory",
            )
            return ServiceResult(response)
        except Exception as e:

            return ServiceResult(e)