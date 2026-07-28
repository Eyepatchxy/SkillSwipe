import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declared_attr


class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, 
        primary_key=True, 
        default=uuid.uuid4
    )

class UserOwnedMixin:
    @declared_attr
    def user_id(cls) -> Mapped[uuid.UUID]: 
        return mapped_column(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            index=True,
            nullable=False
        )

class DocumentOwnedMixin:
    @declared_attr
    def document_id(cls) -> Mapped[uuid.UUID]:
        return mapped_column(
            UUID(as_uuid=True),
            ForeignKey("documents.id"),
            nullable=False
        )

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )

class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
