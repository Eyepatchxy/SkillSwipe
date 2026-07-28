from sqlalchemy import String, Integer, Date, Enum, ForeignKey, UUID, DateTime, Text, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid
from datetime import datetime, date

from app.core.enums import Currency, EmploymentType, RemoteType, JobStatus
from app.db.mixins import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from app.db.types import NAME_LENGTH, DESCRIPTION_LENGTH, URL_LENGTH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.company import Company
    from app.db.models.job_source import JobSource
    from app.db.models.application import Application
    from app.db.models.job_skill import JobSkill

class Job(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="jobs"

    __table_args__= (
        CheckConstraint(
            "max_salary >= min_salary",
            name="ck_job_salary_range",
        ),
        CheckConstraint(
            "min_salary >= 0",
            name="ck_job_min_salary",
        ),
        CheckConstraint(
            "max_salary >= 0",
            name="ck_job_max_salary",
        ),
        CheckConstraint(
            "experience_required_in_years >= 0",
            name="ck_job_experience",
        ),
        CheckConstraint(
            "application_deadline >= posted_date",
            name="ck_job_dates",
        ),
        UniqueConstraint(
            "source_id",
            "external_job_id",
            name="uq_job_external_id",
        )
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job_sources.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    external_job_id: Mapped[str | None] = mapped_column(
        String(NAME_LENGTH),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    description: Mapped[str | None] = mapped_column(String(DESCRIPTION_LENGTH), nullable=True)

    requirements: Mapped[str | None] = mapped_column(Text, nullable=True)

    min_salary: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    max_salary: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    currency: Mapped[Currency] = mapped_column(Enum(Currency), nullable=False, default=Currency.INR)

    employment_type: Mapped[EmploymentType] = mapped_column(Enum(EmploymentType), nullable=False, default=EmploymentType.FULL_TIME, index=True)
    experience_required_in_years: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    location: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    remote_type: Mapped[RemoteType] = mapped_column(Enum(RemoteType), nullable=False, default=RemoteType.ON_SITE)    

    posted_date: Mapped[date] = mapped_column(Date, nullable=False)
    application_deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    job_url: Mapped[str] = mapped_column(String(URL_LENGTH), nullable=False)
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), nullable=False, default=JobStatus.OPEN, index=True)


    company: Mapped["Company"] = relationship(
        back_populates="jobs"
    )
    source: Mapped["JobSource"] = relationship(
        back_populates="jobs"
    )
    applications: Mapped[list["Application"]] = relationship(
        back_populates="job"
    )
    job_skills: Mapped[list["JobSkill"]] = relationship(
        back_populates="job"
    )