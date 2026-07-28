from sqlalchemy import UUID, ForeignKey, Enum, Float, Text, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from app.core.enums import ApplicationStatus
from app.db.mixins import UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.resume import Resume
    from app.db.models.job import Job
    from app.db.models.interview import Interview
    from app.db.models.cover_letter import CoverLetter

class Application(UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="applications"

    __table_args__= (
        UniqueConstraint(
            "user_id",
            "job_id",
            name="uq_application_user_job",
        ),
        CheckConstraint(
            "resume_match_score IS NULL OR (resume_match_score >= 0 AND resume_match_score <= 100)",
            name="ck_application_match_score",
        )
    )

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="SET NULL",),
        nullable=True,
        index=True
    )

    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "resumes.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )

    cover_letter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cover_letters.id",ondelete="SET NULL",),
        nullable=True
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus),
        nullable=False,
        default=ApplicationStatus.PENDING,
        index=True
    )

    resume_match_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


    user: Mapped["User"] = relationship(
        back_populates="applications"
    )
    resume: Mapped["Resume | None"] = relationship(
        back_populates="applications"
    )
    job: Mapped["Job"] = relationship(
        back_populates="applications"
    )
    interviews: Mapped[list["Interview"]] = relationship(
        back_populates="application"
    )
    cover_letter: Mapped["CoverLetter | None"] = relationship(
        back_populates="applications"
    )