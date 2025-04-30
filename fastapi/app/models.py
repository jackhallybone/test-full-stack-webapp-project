from sqlalchemy import (
    Integer,
    String,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    DateTime,
    func,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"created_at={self.created_at!r}, updated_at={self.updated_at!r}"


class SoftDeleteMixin:
    deleted_at = mapped_column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.deleted_at = func.now()

    def __repr__(self) -> str:
        return f"deleted_at={self.deleted_at!r}"


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    email = mapped_column(String, unique=True, nullable=False)
    username = mapped_column(String, nullable=True)


class Project(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "project"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)

    item_statuses = relationship(
        "ItemStatus", back_populates="project", cascade="all, delete-orphan"
    )
    item_locations = relationship(
        "ItemLocation", back_populates="project", cascade="all, delete-orphan"
    )
    item_types = relationship(
        "ItemType", back_populates="project", cascade="all, delete-orphan"
    )
    items = relationship("Item", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Project(id={self.id!r}, name={self.name!r}, {super().__repr__()})"


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

    __table_args__ = (UniqueConstraint("name", "project_id", name="_item_status_uc_name_project"),)

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

    __table_args__ = (UniqueConstraint("name", "project_id", name="_item_location_uc_name_project"),)

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


class Item(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "item"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)

    project_id = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project = relationship("Project", back_populates="items", passive_deletes=True)

    item_status_id = mapped_column(
        ForeignKey("item_status.id", ondelete="SET NULL"), nullable=True, index=True
    )
    item_status = relationship("ItemStatus", back_populates="items")

    item_location_id = mapped_column(
        ForeignKey("item_location.id", ondelete="SET NULL"), nullable=True, index=True
    )
    item_location = relationship("ItemLocation", back_populates="items")

    item_type_id = mapped_column(
        ForeignKey("item_type.id", ondelete="SET NULL"), nullable=True, index=True
    )
    item_type = relationship("ItemType", back_populates="items")

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, {super().__repr__()})"

