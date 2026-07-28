from sqlalchemy import String, Enum, Boolean, CheckConstraint, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from app.core.enums import CompanySize
from app.db.mixins import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from app.db.types import NAME_LENGTH, URL_LENGTH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.industry import Industry
    from app.db.models.location import Location
    from app.db.models.job import Job

class Company(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__= "companies"

    __table_args__= (
        CheckConstraint(
            "website IS NOT NULL OR linkedin_url IS NOT NULL",
            name="ck_company_online_presence",
        ),
    )

    name: Mapped[str] = mapped_column(String(NAME_LENGTH), unique=True, nullable=False, index=True)
    website: Mapped[str | None] = mapped_column(String(URL_LENGTH), nullable=True)

    size: Mapped[CompanySize] = mapped_column(Enum(CompanySize), nullable=False, default=CompanySize.MEDIUM)
    industry_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("industries.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    headquarters_location_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "locations.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True
    )
    linkedin_url: Mapped[str | None] = mapped_column(String(URL_LENGTH), nullable=True)

    logo_url: Mapped[str | None] = mapped_column(String(URL_LENGTH), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


    industry: Mapped["Industry"] = relationship(
        back_populates="companies"
    )
    location: Mapped["Location"] = relationship(
        back_populates="companies"
    )
    jobs: Mapped[list["Job"]] = relationship(
        back_populates="company"
    )