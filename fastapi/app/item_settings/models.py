from sqlalchemy import Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship

from app.core.models import Base


class ItemStatus(Base):
    __tablename__ = "item_status"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    project_id = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), nullable=False, index=True
    )

    project = relationship(
        "Project", back_populates="item_statuses", passive_deletes=True
    )
    items = relationship("Item", back_populates="item_status")

    __table_args__ = (
        UniqueConstraint("name", "project_id", name="_item_status_uc_name_project"),
    )

    def __repr__(self) -> str:
        return f"ItemStatus(id={self.id!r}, name={self.name!r})"

    # TODO: add a check and throw error if self will be deleted while there are items assosiated to it


class ItemLocation(Base):
    __tablename__ = "item_location"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    project_id = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), nullable=False, index=True
    )

    project = relationship(
        "Project", back_populates="item_locations", passive_deletes=True
    )
    items = relationship("Item", back_populates="item_location")

    __table_args__ = (
        UniqueConstraint("name", "project_id", name="_item_location_uc_name_project"),
    )

    def __repr__(self) -> str:
        return f"ItemLocation(id={self.id!r}, name={self.name!r})"

    # TODO: add a check and throw error if self will be deleted while there are items assosiated to it


class ItemType(Base):
    __tablename__ = "item_type"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    order = mapped_column(Integer, nullable=False)
    self_nestable = mapped_column(Boolean, nullable=False, default=False)
    project_id = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), nullable=False, index=True
    )

    project = relationship("Project", back_populates="item_types", passive_deletes=True)
    items = relationship("Item", back_populates="item_type")

    __table_args__ = (
        UniqueConstraint("name", "project_id", name="_item_type_uc_name_project"),
        UniqueConstraint("order", "project_id", name="_item_type_uc_order_project"),
    )

    def __repr__(self) -> str:
        return f"ItemType(id={self.id!r}, name={self.name!r}, order={self.order!r}, self_nestable={self.self_nestable!r})"

    # TODO: add a check and throw error if self will be deleted while there are items assosiated to it