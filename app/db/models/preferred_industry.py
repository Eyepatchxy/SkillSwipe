from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from app.db.mixins import UUIDMixin, TimestampMixin
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.job_preference import JobPreference
    from app.db.models.industry import Industry


class PreferredIndustry(UUIDMixin, TimestampMixin, Base):
    __tablename__="preferred_industries"

    job_preference_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job_preferences.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    industry_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("industries.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )


    job_preference: Mapped["JobPreference"] = relationship(
        back_populates="preferred_industries"
    )
    industry: Mapped["Industry"] = relationship(
        back_populates="preferred_industries"
    )