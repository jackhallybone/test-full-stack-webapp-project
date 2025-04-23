from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db import get_db
from app.schemas import UserCreate, UserRead

app = FastAPI()


@app.post("/users", response_model=UserRead)
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(user, db)


@app.get("/users", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await crud.get_users(db)


@app.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user(user_id, db)


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_user(user_id, db)
