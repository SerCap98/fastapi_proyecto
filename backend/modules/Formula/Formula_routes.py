from fastapi import APIRouter, Body, Depends, Path, Query, status
from databases import Database
from typing import List,Dict
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result


from modules.users.auths.auth_dependencies import get_current_active_user
from modules.users.auths.auth_exceptions import AuthExceptions
from shared.utils.verify_auth import is_authorized
from modules.users.users.user_schemas import  UserInDB

from modules.Formula.Formula_exceptions import FormulaExceptions
from modules.Formula.Formula_services import FormulaService
from modules.Formula.Formula_schemas import Formula,FormulaInDB

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=FormulaInDB, name="Form:create-Formula", status_code=status.HTTP_201_CREATED)
async def create_Formula(
    Form: Formula = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Form:create-Formula"):
        raise AuthExceptions.AuthUnauthorizedException()

    result = await FormulaService(db).create_Formula(Form,current_user)
    return handle_result(result)

@router.get("/get-formula",name="Form:get-formula-by-RawMaterial-and-Product", response_model=FormulaInDB,status_code=status.HTTP_200_OK)
async def get_formula_by_RawMaterial_and_Product(
    raw_material_code: str = Query(..., title="The code of the raw material"),
    product_name: str = Query(..., title="The name of the product"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Form:get-formula-by-RawMaterial-and-Product"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :
        result = await FormulaService(db).get_formula_by_RawMaterial_and_Product(raw_material_code, product_name)
        return handle_result(result)

@router.get("/get-formula/all/", name="Formula:get-all-formula",response_model=Dict,status_code=status.HTTP_200_OK)
async def get_all_formula(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user)
)-> ServiceResult:
    if not is_authorized(current_user, "Formula:get-all-formula"):
        return handle_result(ServiceResult(AuthExceptions.AuthUnauthorizedException()))
    else :

        result = await FormulaService(db).get_all_formula(
        search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,)
        return handle_result(result)