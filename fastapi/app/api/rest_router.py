from fastapi import APIRouter
from app.projects.routes import router as projects_router
from app.item_settings.routes import router as item_settings_router
from app.items.routes import router as items_router

api_router = APIRouter()
api_router.include_router(projects_router)
api_router.include_router(item_settings_router)
api_router.include_router(items_router)