from sqlalchemy import String, Date, Enum, CheckConstraint, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date
import uuid

from app.core.enums import EmploymentType
from app.db.mixins import UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from app.db.types import DESCRIPTION_LENGTH, NAME_LENGTH
from app.db.models.user import User


class WorkExperience(UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "work_experiences"

    __table_args__ = (
        CheckConstraint(
            "end_date IS NULL OR end_date >= start_date",
            name="ck_work_experience_dates",
        ),
        CheckConstraint(
            "(is_current = TRUE AND end_date IS NULL) OR "
            "(is_current = FALSE AND end_date IS NOT NULL)",
            name="ck_work_experience_current_status",
        )
    )

    company: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    title: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)

    employment_type: Mapped[EmploymentType] = mapped_column(Enum(EmploymentType), nullable=False, default=EmploymentType.FULL_TIME)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(nullable=False, default=False)

    description: Mapped[str | None] = mapped_column(String(DESCRIPTION_LENGTH), nullable=True)



    user: Mapped["User"] = relationship(
        back_populates="work_experiences"
    )