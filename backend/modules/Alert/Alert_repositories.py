
from datetime import datetime
from enum import Enum
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB

from modules.Alert.Alert_exceptions import AlertExceptions
from modules.Alert.Alert_schemas import Alert,AlertInDB, AlertList, AlertState

from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository



class AlertRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[Alert]:
        return Alert

    @property
    def _schema_out(self) -> Type[AlertInDB]:
        return AlertInDB

    async def create_alert(self, alert: Alert,current_user: UserInDB) -> AlertInDB:
        from modules.Alert.Alert_sqlstaments import CREATE_ALERT

        factory_id = str(uuid.uuid4())
        current_time = datetime.now()
        try:
            values = {
                "id": factory_id ,
                "id_factory_inventory": alert.id_factory_inventory ,
                "state": alert.state if alert.state else AlertState.PENDING.value,
                "description": alert.description if alert.description else "without description",
                "created_by": current_user.id,
                "created_at": current_time
            }
        
  
            record = await self.db.fetch_one(query=CREATE_ALERT, values=values)
        except Exception as e:
            print(e)
            raise AlertExceptions.AlertInvalidCreateParamsException(e=e)

        result = record_to_dict(record)
        return self._schema_out(**result)
    
    async def get_alert(self, id: UUID) -> AlertInDB:
        from modules.Alert.Alert_sqlstaments import GET_ALERT_BY_ID
        values = {"id": id}
        record = await self.db.fetch_one(query=GET_ALERT_BY_ID, values=values)
        if not record:
            raise AlertExceptions.AlertNotFoundException()
        return self._schema_out(**dict(record))
    
    async def attended_alert(self, id:UUID,current_user: UserInDB) -> AlertInDB:
            from modules.Alert.Alert_sqlstaments import ATTENDED_ALERT_BY_ID
            current_time = datetime.now()
            updated_values = {
                "id": id,
                "state": AlertState.ATTENDED.value,
                "updated_by": current_user.id,
                "updated_at": current_time
            }
            try:
            
                record = await self.db.fetch_one(query=ATTENDED_ALERT_BY_ID, values=updated_values)
               
                return self._schema_out(**dict(record))
            except Exception as e:
                print(e)
                raise AlertExceptions.AlertInvalidUpdateParamsException(e=e)
            
    async def pending_alert(self, id:UUID,current_user: UserInDB) -> AlertInDB:
            from modules.Alert.Alert_sqlstaments import ATTENDED_ALERT_BY_ID
            current_time = datetime.now()
            updated_values = {
                "id": id,
                "state": AlertState.PENDING.value,
                "updated_by": current_user.id,
                "updated_at": current_time
            }
            try:
            
                record = await self.db.fetch_one(query=ATTENDED_ALERT_BY_ID, values=updated_values)
               
                return self._schema_out(**dict(record))
            except Exception as e:
                print(e)
                raise AlertExceptions.AlertInvalidUpdateParamsException(e=e)

    async def delete_alert(self, id: UUID) -> bool:
        from modules.Alert.Alert_sqlstaments import DELETE_ALERT_BY_ID
        try:
            await self.db.execute(query=DELETE_ALERT_BY_ID, values={"id": id})
        except Exception as e:
            raise AlertExceptions.AlertDeleteException()
        return True


    async def get_all_alert(self,
            search: str | None,
            order: str | None,
            direction: str | None
            ) -> List:
            from modules.Alert.Alert_sqlstaments import LIST_ALERT,ALERT_COMPLEMENTS,ALERT_SEARCH
            
            order = order.lower() if order != None else None
            direction = direction.upper() if order != None else None
            values = {}
            sql_sentence = ALERT_COMPLEMENTS(order, direction)
            sql_search = ALERT_SEARCH()
            if not search:
                sql_sentence = LIST_ALERT + sql_sentence
            else:
                sql_sentence = LIST_ALERT + sql_search + sql_sentence
                values["search"] = "%" + search + "%"
            try:
                
                records = await self.db.fetch_all(query=sql_sentence,values=values)
                if len(records) == 0 or not records:
                    return []
       
                return [AlertList(**dict(record)) for record in records]
            

            except Exception as e:
              print(e)
              raise AlertExceptions.AlertListException(e)
        
