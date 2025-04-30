from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column


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
