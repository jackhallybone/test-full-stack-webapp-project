from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from app.core.models import Base
from app.mixins.models import TimestampMixin


class Item(Base, TimestampMixin):
    __tablename__ = "item"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    project_id = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), nullable=False, index=True
    )
    parent_id = mapped_column(ForeignKey("item.id", ondelete="CASCADE"), index=True)
    item_status_id = mapped_column(
        ForeignKey("item_status.id", ondelete="SET NULL"), nullable=True, index=True
    )
    item_location_id = mapped_column(
        ForeignKey("item_location.id", ondelete="SET NULL"), nullable=True, index=True
    )
    item_type_id = mapped_column(
        ForeignKey("item_type.id", ondelete="SET NULL"), nullable=True, index=True
    )

    project = relationship("Project", back_populates="items", passive_deletes=True)
    parent = relationship(
        "Item", back_populates="children", remote_side=[id], passive_deletes=True
    )
    children = relationship(
        "Item",
        back_populates="parent",
    )
    item_status = relationship("ItemStatus", back_populates="items")
    item_location = relationship("ItemLocation", back_populates="items")
    item_type = relationship("ItemType", back_populates="items")

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, {super().__repr__()})"

    # TODO: propergate delete (and/or soft-delete) down the hierarchy
