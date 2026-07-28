from sqlalchemy import String, Date, CheckConstraint, UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date
import uuid

from app.db.mixins import UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from app.db.types import NAME_LENGTH, URL_LENGTH
from app.db.models.user import User
from app.db.models.document import Document


class Certification(UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "certifications"

    __table_args__= (
        CheckConstraint(
            "expiry_date IS NULL OR expiry_date >= issue_date",
            name="ck_certification_dates"
        ),  
    )

    document_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="RESTRICT"),
        nullable=True,
        unique=True,
        index=True
    )

    name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    issuer: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)

    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    credential_id: Mapped[str | None] = mapped_column(String(NAME_LENGTH), unique=True, nullable=True)
    credential_url: Mapped[str | None] = mapped_column(String(URL_LENGTH), nullable=True)


    user: Mapped["User"] = relationship(
        back_populates="certifications"
    )
    document: Mapped["Document"] = relationship(
        back_populates="certification"
    )