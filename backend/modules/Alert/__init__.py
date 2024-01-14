from fastapi import APIRouter

from modules.Alert.Alert_routes import router as alert_router

alerts_router = APIRouter(
    prefix="/alert",
    tags=["alert"],
    responses={404: {"description": "Not found"}},
)

# Rutas específicas de factory
alerts_router.include_router(alert_router)