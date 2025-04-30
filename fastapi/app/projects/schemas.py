from typing import TYPE_CHECKING, Annotated

from pydantic import ConfigDict, StringConstraints

from app.core.schemas import BaseModel
from app.mixins.schemas import TimestampMixinBase

if TYPE_CHECKING:
    from app.item_settings.schemas import ItemStatusRead, ItemLocationRead, ItemTypeRead
    from app.items.schemas import ItemRead


class ProjectBase(BaseModel, TimestampMixinBase):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
    item_statuses: list["ItemStatusRead"]
    item_locations: list["ItemLocationRead"]
    item_types: list["ItemTypeRead"]
    items: list["ItemRead"]

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):
    name: (
        Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] | None
    ) = None


