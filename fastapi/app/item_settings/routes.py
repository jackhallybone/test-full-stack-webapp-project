from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.item_settings.crud import item_status_crud, item_location_crud, item_type_crud
from app.item_settings.models import ItemStatus, ItemLocation, ItemType
from app.item_settings.schemas import ItemStatusCreate, ItemStatusRead, ItemStatusUpdate, ItemLocationCreate, ItemLocationRead, ItemLocationUpdate, ItemTypeCreate, ItemTypeRead, ItemTypeUpdate

router = APIRouter()


@router.post("/item_status/", response_model=ItemStatusRead)
async def create_item_status(data: ItemStatusCreate, db: AsyncSession = Depends(get_db)) -> ItemStatus:
    return await item_status_crud.create(db=db, data=data)


@router.get("/item_status/", response_model=list[ItemStatusRead])
async def get_item_statuses(db: AsyncSession = Depends(get_db)) -> list[ItemStatus]:
    return await item_status_crud.read_many(db=db)


@router.get("/item_status/{id}", response_model=ItemStatusRead)
async def get_item_status(id: int, db: AsyncSession = Depends(get_db)) -> ItemStatus:
    return await item_status_crud.read_one(db=db, id=id)


@router.put("/item_status/{id}", response_model=ItemStatusRead)
async def update_item_status(id: int, data: ItemStatusUpdate, db: AsyncSession = Depends(get_db)) -> ItemStatus:
    return await item_status_crud.update(db=db, id=id, data=data)


@router.delete("/item_status/{id}", status_code=204)
async def delete_item_status(id: int, db: AsyncSession = Depends(get_db)) -> None:
    return await item_status_crud.delete(db=db, id=id)


@router.post("/item_location/", response_model=ItemLocationRead)
async def create_item_location(data: ItemLocationCreate, db: AsyncSession = Depends(get_db)) -> ItemLocation:
    return await item_location_crud.create(db=db, data=data)


@router.get("/item_location/", response_model=ItemLocationRead)
async def get_item_locations(db: AsyncSession = Depends(get_db)) -> list[ItemLocation]:
    return await item_location_crud.read_many(db=db)


@router.get("/item_location/{id}", response_model=ItemLocationRead)
async def get_item_location(id: int, db: AsyncSession = Depends(get_db)) -> ItemLocation:
    return await item_location_crud.read_one(db=db, id=id)


@router.put("/item_location/{id}", response_model=ItemLocationRead)
async def update_item_location(id: int, data: ItemLocationUpdate, db: AsyncSession = Depends(get_db)) -> ItemLocation:
    return await item_location_crud.update(db=db, id=id, data=data)


@router.delete("/item_location/{id}", status_code=204)
async def delete_item_location(id: int, db: AsyncSession = Depends(get_db)) -> None:
    return await item_location_crud.delete(db=db, id=id)


@router.post("/item_type/", response_model=ItemTypeRead)
async def create_item_type(data: ItemTypeCreate, db: AsyncSession = Depends(get_db)) -> ItemType:
    return await item_type_crud.create(db=db, data=data)


@router.get("/item_type/", response_model=ItemTypeRead)
async def get_item_types(db: AsyncSession = Depends(get_db)) -> list[ItemType]:
    return await item_type_crud.read_many(db=db)


@router.get("/item_type/{id}", response_model=ItemTypeRead)
async def get_item_type(id: int, db: AsyncSession = Depends(get_db)) -> ItemType:
    return await item_type_crud.read_one(db=db, id=id)


@router.put("/item_type/{id}", response_model=ItemTypeRead)
async def update_item_type(id: int, data: ItemTypeUpdate, db: AsyncSession = Depends(get_db)) -> ItemType:
    return await item_type_crud.update(db=db, id=id, data=data)


@router.delete("/item_type/{id}", status_code=204)
async def delete_item_type(id: int, db: AsyncSession = Depends(get_db)) -> None:
    return await item_type_crud.delete(db=db, id=id)