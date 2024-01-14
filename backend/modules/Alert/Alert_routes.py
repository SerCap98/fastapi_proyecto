
from fastapi import APIRouter, Body, Depends, Path, status
from databases import Database
from uuid import UUID
from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized


from modules.Alert.Alert_schemas import AlertList, AlertInDB,Alert
from modules.Alert.Alert_services import AlertService


from shared.utils.service_result import ServiceResult, handle_result
from shared.core.db.db_dependencies import get_database
from typing import List,Dict
from modules.users.users.user_schemas import  UserInDB


router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=AlertInDB, name="Alert:create-alert", status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert: Alert = Body(..., embed=True),  
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Alert:create-alert"):
        raise AuthExceptions.AuthUnauthorizedException()
   
    result = await AlertService(db).create_alert(alert,current_user)
    return handle_result(result)

@router.get("/{id}",name="Alert:get-alert", response_model=AlertInDB,status_code=status.HTTP_200_OK)
async def get_alert(
    id: UUID = Path(..., title="The id of the alert to retrieve"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Alert:get-alert"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await AlertService(db).get_alert(id)
        return handle_result(result)
    
@router.get("/all/", name="Alert:get-all-alert",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_alert(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:

    if not is_authorized(current_user, "Alert:get-all-alert"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :

        result = await AlertService(db).get_all_alert( 
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)   
    


    
@router.delete("/{id}", response_model=dict, name="Alert:delete-alert",status_code=status.HTTP_200_OK)
async def delete_factory_by_identifier(
    id: UUID = Path(..., title="The id of the alert to delete"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Alert:delete-alert"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await AlertService(db).delete_alert(id)
        return handle_result(result)

@router.put("/update-alert/attended/{id}", response_model=AlertInDB, name="Alert:attended-Alert",status_code=status.HTTP_200_OK)
async def attended_alert(
    id: UUID = Path(..., title="The id of the alert to attended"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Alert:attended-Alert"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await AlertService(db).attended_alert(id,current_user)
        return handle_result(result)
    
@router.put("/update-alert/pending/{id}", response_model=AlertInDB, name="Alert:pending-Alert",status_code=status.HTTP_200_OK)
async def pending_alert(
    id: UUID = Path(..., title="The id of the alert to pending"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Alert:pending-Alert"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await AlertService(db).pending_alert(id,current_user)
        return handle_result(result)