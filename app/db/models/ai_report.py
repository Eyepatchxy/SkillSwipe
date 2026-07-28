from sqlalchemy import ForeignKey, UUID, Enum, Float, Text, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from app.core.enums import AnalysisType
from app.db.base import Base
from app.db.mixins import UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.resume import Resume
    from app.db.models.ai_model import AIModel

class AIReport(UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="ai_reports"

    __table_args__= (
        CheckConstraint(
            "score >= 0 AND score <= 100",
            name="ck_ai_report_score",
        ),
        UniqueConstraint(
            "resume_id",
            "model_id",
            "analysis_type",
            name="uq_ai_report_resume_model_analysis",
        )
    )

    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    model_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ai_models.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    analysis_type: Mapped[AnalysisType] = mapped_column(
        Enum(AnalysisType),
        nullable=False,
        default=AnalysisType.LIGHT,
        index=True
    )

    score: Mapped[float] = mapped_column(Float, nullable=False)

    summary: Mapped[str] = mapped_column(Text, nullable=False)

    recommendations: Mapped[str] = mapped_column(Text, nullable=False)


    resume: Mapped["Resume"] = relationship(
        back_populates="ai_reports"
    )
    ai_model: Mapped["AIModel"] = relationship(
        back_populates="ai_reports"
    )