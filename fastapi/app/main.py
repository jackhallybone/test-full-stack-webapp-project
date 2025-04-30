from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter

from app import crud
from app.db import get_db
from app.graphql.context import get_context_for_request
from app.graphql.schema import schema
from app.models import User
from app.schemas import UserCreate, UserRead, DeleteResponse

app = FastAPI()

graphql_app = GraphQLRouter(schema, context_getter=get_context_for_request)
app.include_router(graphql_app, prefix="/graphql")


@app.post("/users", response_model=UserRead)
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    return await crud.create_user(user, db)


@app.get("/users", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)) -> User:
    return await crud.get_users(db)


@app.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    return await crud.get_user(user_id, db)


@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> DeleteResponse:
    return await crud.delete_user(user_id, db)
