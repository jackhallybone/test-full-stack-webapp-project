from fastapi import FastAPI
from app.api.rest_router import api_router

from app.projects.schemas import ProjectRead
from app.item_settings.schemas import (
    ItemStatusCreate,
    ItemStatusRead,
    ItemLocationCreate,
    ItemLocationRead,
    ItemTypeCreate,
    ItemTypeRead
)
from app.items.schemas import ItemCreate, ItemRead

ItemCreate.model_rebuild()
ItemRead.model_rebuild()
ItemStatusCreate.model_rebuild()
ItemStatusRead.model_rebuild()
ItemLocationCreate.model_rebuild()
ItemLocationRead.model_rebuild()
ItemTypeCreate.model_rebuild()
ItemTypeRead.model_rebuild()
ProjectRead.model_rebuild()

app = FastAPI()
app.include_router(api_router)
