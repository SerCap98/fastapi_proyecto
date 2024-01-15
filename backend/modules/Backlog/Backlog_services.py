#from shared.utils.events import EventBus, OrderUpdatedEvent
from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB


from modules.Backlog.Backlog_exceptions import  BacklogExceptions
from modules.Backlog.Backlog_repositories import BacklogRepository
from modules.Backlog.Backlog_schemas import  Backlog,BacklogInDB, BacklogList, BacklogState

from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID


class BacklogService:
    def __init__(self, db: Database):
        self.db = db
        #EventBus.subscribe(OrderUpdatedEvent, self.handle_order_update)


    async def create_backlog(self, backlog: Backlog,current_user: UserInDB) -> ServiceResult:
        backlog_repo = BacklogRepository(self.db)
        try:

            backlog = await backlog_repo.create_backlog(backlog,current_user)
            return ServiceResult(backlog,)

        except Exception as e:
            return ServiceResult(e)

    async def get_backlog(self, id: UUID) -> ServiceResult:
        try:
            backlog = await BacklogRepository(self.db).get_backlog(id)
            return ServiceResult(backlog)
        except Exception  as e:

            return ServiceResult(e)
        
    async def attended_backlog(self, id: UUID, current_user: UserInDB) -> ServiceResult:
        try:
            exist_backlog=await self.get_backlog(id)
            if not exist_backlog.success:return exist_backlog
            backlog = await BacklogRepository(self.db).attended_backlog(id,current_user)
            return ServiceResult(backlog)
        except Exception as e:
            return ServiceResult(e)

    async def pending_backlog(self, id: UUID, current_user: UserInDB) -> ServiceResult:
        try:
            exist_backlog=await self.get_backlog(id)
            if not exist_backlog.success:return exist_backlog
            backlog = await BacklogRepository(self.db).pending_backlog(id,current_user)
            return ServiceResult(backlog)
        except Exception as e:
            return ServiceResult(e)
    async def delete_backlog(self, id: UUID) -> ServiceResult:
        try:

            exist_backlog=await self.get_backlog(id)
            if not exist_backlog.success:return exist_backlog

            await BacklogRepository(self.db).delete_backlog(id)
            return ServiceResult({"message": "backlog successfully removed"})
        except Exception as e:
            return ServiceResult(e)

    async def get_all_backlog(self, 
            search: str | None,
            page_num: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: str = None,
        ) -> ServiceResult:
            try:

                backlog = await BacklogRepository(self.db).get_all_backlog(search,order,direction)

                backlog_list = [BacklogList(**item.dict()) for item in backlog]

                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=backlog_list,
                    route=f"{API_PREFIX}/Backlog",
                )

                return ServiceResult(response)
            except Exception as e:

                return ServiceResult(e)

    """ async def handle_order_update(self, event: OrderUpdatedEvent):
        if event.new_quantity < event.min_quantity:

            backlog = Backlog(
                id_order_product=event.order_product_id,
                state=BacklogState.PENDING,
                description="Pedido pendiente"
            )
            await self.create_backlog(backlog, event.current_user) """