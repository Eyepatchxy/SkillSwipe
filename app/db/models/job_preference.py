from sqlalchemy import Enum, Integer, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import EmploymentType, RemoteType, Currency
from app.db.mixins import UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.preferred_role import PreferredRole
    from app.db.models.preferred_industry import PreferredIndustry
    from app.db.models.preferred_location import PreferredLocation

class JobPreference(UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="job_preferences"

    __table_args__= (
        CheckConstraint(
            "maximum_salary >= minimum_salary",
            name="ck_job_preference_salary_range"
        ),
        CheckConstraint(
            "minimum_salary >= 0",
            name="ck_job_preference_min_salary",
        ),
        CheckConstraint(
            "maximum_salary >= 0",
            name="ck_job_preference_max_salary",
        ),
    )

    employment_type: Mapped[EmploymentType] = mapped_column(Enum(EmploymentType), nullable=False, default=EmploymentType.FULL_TIME)

    minimum_salary: Mapped[int] = mapped_column(Integer, nullable=False)
    maximum_salary: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[Currency] = mapped_column(Enum(Currency), nullable=False, default=Currency.INR)

    remote_preference: Mapped[RemoteType] = mapped_column(Enum(RemoteType), nullable=False, default=RemoteType.REMOTE)
    requires_visa_sponsorship: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    willing_to_relocate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


    user: Mapped["User"] = relationship(
        back_populates="job_preferences"
    )
    preferred_roles: Mapped[list["PreferredRole"]] = relationship(
        back_populates="job_preference"
    )
    preferred_industries: Mapped[list["PreferredIndustry"]] = relationship(
        back_populates="job_preference"
    )
    preferred_locations: Mapped[list["PreferredLocation"]] = relationship(
        back_populates="job_preference"
    )