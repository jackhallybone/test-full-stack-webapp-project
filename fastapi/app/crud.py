from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User
from app.schemas import DeleteResponse, UserCreate, UserUpdate


async def create_user(user_data: UserCreate, db: AsyncSession) -> User:
    # Create a user
    new_user = User(**user_data.dict())

    # Commit the user to the database and return the new user
    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError as e:
        if "email" in str(e.orig) and "unique" in str(e.orig):
            raise HTTPException(status_code=400, detail="Email already in use.")
        raise HTTPException(status_code=500, detail="Error creating the user.")
    await db.refresh(new_user)
    return new_user


async def get_users(db: AsyncSession) -> list[User]:
    # Get all users from the database and return all users
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user(user_id: int, db: AsyncSession) -> User:
    # Get the user from the database or raise a 404
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return the user
    return user


async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession) -> User:
    # Get the user from the database or raise a 404
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only the fields provided
    for field, value in user_data.dict(exclude_none=True).items():
        setattr(user, field, value)

    # Commit the changes to the database and return the updated user
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as e:
        if "email" in str(e.orig) and "unique" in str(e.orig):
            raise HTTPException(status_code=400, detail="Email already in use.")
        raise HTTPException(status_code=500, detail="Error updating the user.")
    await db.refresh(user)
    return user


async def delete_user(user_id: int, db: AsyncSession) -> DeleteResponse:
    # Get the user from the database or raise a 404
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user from the database and return a success message
    await db.delete(user)
    await db.commit()
    return DeleteResponse(f"User with ID {user_id} successfully deleted")
