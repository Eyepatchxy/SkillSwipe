from sqlalchemy import String, Boolean, Integer, Text, UUID, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from app.db.mixins import UUIDMixin, UserOwnedMixin, DocumentOwnedMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from app.db.types import NAME_LENGTH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.document import Document
    from app.db.models.application import Application
    from app.db.models.ai_report import AIReport
    from app.db.models.resume_skill import ResumeSkill


class Resume(UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "resumes"

    __table_args__= (
        CheckConstraint(
            "version > 0",
            name="ck_resume_version_positive"
        ),
        UniqueConstraint(
            "user_id",
            "name",
            "version",
            name="uq_resume_user_name_version"
        )
    )
   
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "documents.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    parsed_text: Mapped[str] = mapped_column(Text, nullable=False)

    version: Mapped[int] = mapped_column(Integer, nullable=False)

    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)



    user: Mapped["User"] = relationship(
        back_populates="resumes"
    )
    document: Mapped["Document"] = relationship(
        back_populates="resume"
    )
    applications: Mapped[list["Application"]] = relationship(
        back_populates="resume"
    )
    ai_reports: Mapped[list["AIReport"]] = relationship(
        back_populates="resume"
    )
    resume_skills: Mapped[list["ResumeSkill"]] = relationship(
        back_populates="resume"
    )