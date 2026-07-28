from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDMixin, SoftDeleteMixin
from app.core.enums import AccountStatus, SubscriptionPlan
from app.db.types import EMAIL_LENGTH, PASSWORD_HASH_LENGTH, NAME_LENGTH, PHONE_LENGTH, URL_LENGTH

from sqlalchemy import String, Date, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.document import Document
    from app.db.models.resume import Resume
    from app.db.models.work_experience import WorkExperience
    from app.db.models.education import Education
    from app.db.models.certification import Certification
    from app.db.models.application import Application
    from app.db.models.job_preference import JobPreference
    from app.db.models.notification import Notification
    from app.db.models.saved_job import SavedJob
    from app.db.models.activity_log import ActivityLog
    

class User(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(EMAIL_LENGTH), 
        unique=True, 
        index=True, 
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(PASSWORD_HASH_LENGTH), 
        nullable=False
    )

    first_name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    last_name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(PHONE_LENGTH), unique=True, nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)

    profile_picture_url: Mapped[str] = mapped_column(String(URL_LENGTH), nullable=True)

    account_status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus), nullable=False, default=AccountStatus.ACTIVE)
    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(Enum(SubscriptionPlan), nullable=False, default=SubscriptionPlan.FREE)

    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)



    documents: Mapped[list["Document"]] = relationship(
        back_populates="user",
    )

    resumes: Mapped[list["Resume"]] = relationship(
        back_populates="user"
    )

    work_experiences: Mapped[list["WorkExperience"]] = relationship(
        back_populates="user"
    )

    educations: Mapped[list["Education"]] = relationship(
        back_populates="user"
    )

    certifications: Mapped[list["Certification"]] = relationship(
        back_populates="user"
    )

    applications: Mapped[list["Application"]] = relationship(
        back_populates="user"
    )

    job_preferences: Mapped[list["JobPreference"]] = relationship(
        back_populates="user"
    )

    notifications: Mapped[list["Notification"]] =  relationship(
        back_populates="user"
    )

    saved_jobs: Mapped[list["SavedJob"]] =  relationship(
        back_populates="user"
    )

    activity_logs: Mapped[list["ActivityLog"]] = relationship(
        back_populates="user"
    )