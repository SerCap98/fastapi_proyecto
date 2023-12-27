from fastapi import APIRouter
from modules.users import users_router
from modules.MateriasPrimas import materias_primas_router

router = APIRouter()

router.include_router(users_router)
router.include_router(materias_primas_router)
