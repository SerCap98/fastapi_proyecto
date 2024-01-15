from fastapi import APIRouter

from modules.Backlog.Backlog_routes import router as Backlog_router

Backlogs_router = APIRouter(
    prefix="/Backlog",
    tags=["Backlog"],
    responses={404: {"description": "Not found"}},
)

# Rutas específicas de backlog
Backlogs_router.include_router(Backlog_router)