
from fastapi import APIRouter, Body, Depends, Path, status
from databases import Database
from uuid import UUID
from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized


from modules.Backlog.Backlog_schemas import BacklogList, BacklogInDB,Backlog
from modules.Backlog.Backlog_services import BacklogService


from shared.utils.service_result import ServiceResult, handle_result
from shared.core.db.db_dependencies import get_database
from typing import List,Dict
from modules.users.users.user_schemas import  UserInDB


router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=BacklogInDB, name="Backlog:create-backlog", status_code=status.HTTP_201_CREATED)
async def create_backlog(
    backlog: Backlog = Body(..., embed=True),  
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Backlog:create-backlog"):
        raise AuthExceptions.AuthUnauthorizedException()
   
    result = await BacklogService(db).create_backlog(backlog,current_user)
    return handle_result(result)

@router.get("/{id}",name="Backlog:get-backlog", response_model=BacklogInDB,status_code=status.HTTP_200_OK)
async def get_backlog(
    id: UUID = Path(..., title="The id of the backlog to retrieve"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Backlog:get-backlog"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await BacklogService(db).get_backlog(id)
        return handle_result(result)
    
@router.get("/all/", name="Backlog:get-all-backlog",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_backlog(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:

    if not is_authorized(current_user, "Backlog:get-all-backlog"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :

        result = await BacklogService(db).get_all_backlog( 
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)   

@router.delete("/{id}", response_model=dict, name="Backlog:delete-backlog",status_code=status.HTTP_200_OK)
async def delete_product_by_name(
    id: UUID = Path(..., title="The id of the backlog to delete"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Backlog:delete-backlog"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await BacklogService(db).delete_backlog(id)
        return handle_result(result)

@router.put("/update-backlog/attended/{id}", response_model=BacklogInDB, name="Backlog:attended-Backlog",status_code=status.HTTP_200_OK)
async def attended_backlog(
    id: UUID = Path(..., title="The id of the backlog to attended"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Backlog:attended-Backlog"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await BacklogService(db).attended_backlog_updte(id,current_user)
        return handle_result(result)

@router.put("/update-backlog/pending/{id}", response_model=BacklogInDB, name="Backlog:pending-Backlog",status_code=status.HTTP_200_OK)
async def pending_backlog(
    id: UUID = Path(..., title="The id of the backlog to pending"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Backlog:pending-Backlog"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await BacklogService(db).pending_backlog(id,current_user)
        return handle_result(result)