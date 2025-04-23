from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    username: str | None = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    username: str | None = None
