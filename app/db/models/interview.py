from sqlalchemy import UUID, ForeignKey, Integer, DateTime, Enum, Text, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid
from datetime import datetime

from app.core.enums import InterviewMode, InterviewStatus
from app.db.mixins import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.application import Application

class Interview(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="interviews"

    __table_args__= (
        UniqueConstraint(
            "application_id",
            "round_number",
            name="uq_interview_application_round",
        ),
        CheckConstraint(
            "round_number > 0",
            name="ck_interview_round_positive",
        )
    )

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    round_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    mode: Mapped[InterviewMode] = mapped_column(Enum(InterviewMode), nullable=False, default=InterviewMode.VIDEO_CALL)

    status: Mapped[InterviewStatus] = mapped_column(Enum(InterviewStatus), nullable=False, default=InterviewStatus.SCHEDULED, index=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


    application: Mapped["Application"] = relationship(
        back_populates="interviews"
    )