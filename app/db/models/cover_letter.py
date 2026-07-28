from sqlalchemy import Boolean, Text, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from app.db.mixins import UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.document import Document
    from app.db.models.application import Application

class CoverLetter(UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="cover_letters"

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey(
            "jobs.id",
            ondelete="RESTRICT"
        ), 
        nullable=False,
    )

    document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="RESTRICT"),
        nullable=True,
        unique=True
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    generated_by_ai: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    document: Mapped["Document"] = relationship(
        back_populates="cover_letter"
    )
    applications: Mapped[list["Application"]] = relationship(
        back_populates="cover_letter"
    )