from sqlalchemy import String, CheckConstraint, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from app.db.mixins import UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from app.db.types import DESCRIPTION_LENGTH, NAME_LENGTH
from app.db.models.user import User


class Education(UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "education"

    __table_args__= (
        CheckConstraint(
            "end_year IS NULL OR end_year >= start_year",
            name="ck_education_years"
        ),
    )

    institution: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    degree: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)

    field_of_study: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)

    start_year: Mapped[int] = mapped_column(nullable=False)
    end_year: Mapped[int | None] = mapped_column(nullable=True)

    grade: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)

    description: Mapped[str | None] = mapped_column(String(DESCRIPTION_LENGTH), nullable=True)


    user: Mapped["User"] = relationship(
        back_populates="educations"
    )