from typing import TYPE_CHECKING, Annotated

from pydantic import ConfigDict, StringConstraints

from app.core.schemas import BaseModel

if TYPE_CHECKING:
    from app.projects.schemas import ProjectRead
    from app.items.schemas import ItemRead


class ItemStatusBase(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    project: "ProjectRead"


class ItemStatusCreate(ItemStatusBase):
    pass


class ItemStatusRead(ItemStatusBase):
    id: int
    items: list["ItemRead"]

    model_config = ConfigDict(from_attributes=True)


class ItemStatusUpdate(BaseModel):
    name: (
        Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] | None
    ) = None
    project_id: int | None = None


class ItemLocationBase(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    project: "ProjectRead"


class ItemLocationCreate(ItemLocationBase):
    pass


class ItemLocationRead(ItemLocationBase):
    id: int
    items: list["ItemRead"]

    model_config = ConfigDict(from_attributes=True)


class ItemLocationUpdate(BaseModel):
    name: (
        Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] | None
    ) = None
    order: int
    self_nestable: bool
    project_id: int | None = None


class ItemTypeBase(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    project: "ProjectRead"


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemTypeRead(ItemTypeBase):
    id: int
    items: list["ItemRead"]

    model_config = ConfigDict(from_attributes=True)


class ItemTypeUpdate(BaseModel):
    name: (
        Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] | None
    ) = None
    order: int | None = None
    self_nestable: bool | None = None
    project_id: int | None = None


