from shared.utils.events import EventBus, InventoryUpdatedEvent
from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB


from modules.Alert.Alert_exceptions import  AlertExceptions

from modules.Alert.Alert_repositories import AlertRepository
from modules.Alert.Alert_schemas import  Alert,AlertInDB, AlertList, AlertState

from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID


class AlertService:
    def __init__(self, db: Database):
        self.db = db
        EventBus.subscribe(InventoryUpdatedEvent, self.handle_inventory_update)


    async def create_alert(self, alert: Alert,current_user: UserInDB) -> ServiceResult:
        alert_repo = AlertRepository(self.db)
        try:
          
            alert = await alert_repo.create_alert(alert,current_user)
            return ServiceResult(alert,)

        except Exception as e:
            return ServiceResult(e)
        
    async def get_alert(self, id: UUID) -> ServiceResult:
        try:
            alert = await AlertRepository(self.db).get_alert(id)
            return ServiceResult(alert)
        except Exception  as e:

            return ServiceResult(e)
        
    async def attended_alert(self, id: UUID, current_user: UserInDB) -> ServiceResult:
        try:
            exist_alert=await self.get_alert(id)
            if not exist_alert.success:return exist_alert
            alert = await AlertRepository(self.db).attended_alert(id,current_user)
            return ServiceResult(alert)
        except Exception as e:
            return ServiceResult(e)

    async def pending_alert(self, id: UUID, current_user: UserInDB) -> ServiceResult:
        try:
            exist_alert=await self.get_alert(id)
            if not exist_alert.success:return exist_alert
            alert = await AlertRepository(self.db).pending_alert(id,current_user)
            return ServiceResult(alert)
        except Exception as e:
            return ServiceResult(e)
    async def delete_alert(self, id: UUID) -> ServiceResult:
        try:

            exist_alert=await self.get_alert(id)
            if not exist_alert.success:return exist_alert

            await AlertRepository(self.db).delete_alert(id)
            return ServiceResult({"message": "alert successfully removed"})
        except Exception as e:
            return ServiceResult(e)
        
    async def handle_inventory_update(self, event: InventoryUpdatedEvent):
     
        if event.new_quantity < event.min_quantity:

            alert = Alert(
                id_factory_inventory=event.inventory_id,  
                state=AlertState.PENDING, 
                description="Quantity below the minimum required"
            )
            print("yeees")
            await self.create_alert(alert, event.current_user)