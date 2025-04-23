from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User
from app.schemas import UserCreate, UserUpdate


async def create_user(user_create: UserCreate, db: AsyncSession):
    # Create a user
    new_user = User(**user_create.dict())

    # Commit the user to the database and return the new user
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_users(db: AsyncSession):
    # Get all users from the database and return all users
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user(user_id: int, db: AsyncSession):
    # Get the user from the database or raise a 404
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return the user
    return user


async def update_user(user_id: int, user_update: UserUpdate, db: AsyncSession):
    # Get the user from the database or raise a 404
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only the fields provided
    if user_update.name:
        user.name = user_update.name
    if user_update.email:
        user.email = user_update.email
    if user_update.username:
        user.username = user_update.username

    # Commit the changes to the database and return the updated user
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user_id: int, db: AsyncSession):
    # Get the user from the database or raise a 404
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user from the database and return a success message
    await db.delete(user)
    await db.commit()
    return {"message": f"User with ID {user_id} deleted"}
