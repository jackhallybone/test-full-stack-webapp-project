from typing import Type, TypeVar

import strawberry
from pydantic import BaseModel

from app.crud import create_user, delete_user, get_user, get_users, update_user
from app.graphql.types import (DeleteResponseType, UserCreateInput, UserType,
                               UserUpdateInput)
from app.models import Base
from app.schemas import UserCreate, UserUpdate

StrawberryType = TypeVar("StrawberryType")
StrawberryInput = TypeVar("StrawberryInput")


def sqlalchemy_to_strawberry(
    sqlalchemy_model: Base, strawberry_cls: Type[StrawberryType]
) -> StrawberryType:
    """Convert sqlalchemy model to a strawberry type using the fields defined in the destination."""
    fields = {
        field.name: getattr(sqlalchemy_model, field.name)
        for field in strawberry_cls.__strawberry_definition__.fields
        if hasattr(sqlalchemy_model, field.name)
    }
    return strawberry_cls(**fields)


def strawberry_to_pydantic(
    strawberry_input: StrawberryInput, pydantic_cls: Type[BaseModel]
) -> BaseModel:
    """Convert strawberry type to a pydantic schema using the fields defined in the destination."""
    data = {
        field_name: getattr(strawberry_input, field_name)
        for field_name in pydantic_cls.__fields__.keys()
        if hasattr(strawberry_input, field_name)
    }
    return pydantic_cls(**data)


@strawberry.type
class Query:

    @strawberry.field
    async def users(self, info) -> list[UserType]:
        db = info.context.db
        users = await get_users(db)
        return [sqlalchemy_to_strawberry(user, UserType) for user in users]

    @strawberry.field
    async def user(self, info, id: int) -> UserType | None:
        db = info.context.db
        user = await get_user(id, db)
        return sqlalchemy_to_strawberry(user, UserType)


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_user(self, info, input: UserCreateInput) -> UserType:
        db = info.context.db
        user_create = strawberry_to_pydantic(input, UserCreate)
        user = await create_user(user_create, db)
        return sqlalchemy_to_strawberry(user, UserType)

    @strawberry.mutation
    async def update_user(self, info, id: int, input: UserUpdateInput) -> UserType:
        db = info.context.db
        user_update = strawberry_to_pydantic(input, UserUpdate)
        user = await update_user(id, user_update, db)
        return sqlalchemy_to_strawberry(user, UserType)

    @strawberry.mutation
    async def delete_user(self, info, id: int) -> DeleteResponseType:
        db = info.context.db
        result = await delete_user(id, db)
        return sqlalchemy_to_strawberry(result, DeleteResponseType)


schema = strawberry.Schema(query=Query, mutation=Mutation)
