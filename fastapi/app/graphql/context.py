from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi.context import BaseContext

from app.db import get_db


class Context(BaseContext):
    def __init__(self, db: AsyncSession):
        self.db = db


async def get_context_for_request(db: AsyncSession = Depends(get_db)) -> Context:
    return Context(db=db)
