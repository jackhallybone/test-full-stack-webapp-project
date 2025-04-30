from typing import TYPE_CHECKING, Annotated, Optional

from pydantic import ConfigDict, StringConstraints

from app.core.schemas import BaseModel
from app.mixins.schemas import TimestampMixinBase

if TYPE_CHECKING:
    from app.projects.schemas import ProjectRead
    from app.item_settings.schemas import ItemLocationRead, ItemStatusRead, ItemTypeRead
    from app.items.schemas import ItemRead


class ItemBase(BaseModel, TimestampMixinBase):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    project: "ProjectRead"
    parent: Optional["ItemRead"] = None
    item_status: "ItemStatusRead"
    item_location: "ItemLocationRead"
    item_type: "ItemTypeRead"


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    children: list["ItemRead"]

    model_config = ConfigDict(from_attributes=True)


class ItemUpdate(BaseModel):
    name: (
        Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] | None
    ) = None
    project_id: int | None = None
    parent_id: int | None = None
    item_status_id: int | None = None
    item_location_id: int | None = None
    item_type_id: int | None = None


