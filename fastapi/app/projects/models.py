from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship

from app.core.models import Base
from app.mixins.models import TimestampMixin


class Project(Base, TimestampMixin):
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

    # TODO: propergate delete (and/or soft-delete) to items
