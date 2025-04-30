from typing import Type, TypeVar, Generic

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models import Base
from app.core.schemas import BaseModel

ModelType = TypeVar("ModelType", bound=Base)
SchemaCreateType = TypeVar("SchemaCreateType", bound=BaseModel)
SchemaUpdateType = TypeVar("SchemaUpdateType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaCreateType, SchemaUpdateType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, db: AsyncSession, data: SchemaCreateType) -> ModelType:
        obj = self.model(**data.dict())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def read_one(self, db: AsyncSession, id: int) -> ModelType:
        result = await db.execute(select(self.model).where(self.model.id == id))
        obj = result.scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        return obj

    async def read_many(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(
        self, db: AsyncSession, id: int, data: SchemaUpdateType
    ) -> ModelType:
        obj = await self.read_one(db, id)
        for field, value in data.dict(exclude_none=True).items():
            setattr(obj, field, value)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, id: int) -> None:
        user = await self.read_one(db, id)
        await db.delete(user)
        await db.commit()
        # return Response(status_code=204)
