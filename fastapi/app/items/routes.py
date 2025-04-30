from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.items.crud import item_crud
from app.items.models import Item
from app.items.schemas import ItemCreate, ItemRead, ItemUpdate

router = APIRouter()


@router.post("/items/", response_model=ItemRead)
async def create_item(data: ItemCreate, db: AsyncSession = Depends(get_db)) -> Item:
    return await item_crud.create(db=db, data=data)


@router.get("/items/", response_model=list[ItemRead])
async def get_items(db: AsyncSession = Depends(get_db)) -> list[Item]:
    return await item_crud.read_many(db=db)


@router.get("/items/{id}", response_model=ItemRead)
async def get_item(id: int, db: AsyncSession = Depends(get_db)) -> Item:
    return await item_crud.read_one(db=db, id=id)


@router.put("/items/{id}", response_model=ItemRead)
async def update_item(id: int, data: ItemUpdate, db: AsyncSession = Depends(get_db)) -> Item:
    return await item_crud.update(db=db, id=id, data=data)


@router.delete("/items/{id}", status_code=204)
async def delete_item(id: int, db: AsyncSession = Depends(get_db)) -> None:
    return await item_crud.delete(db=db, id=id)
