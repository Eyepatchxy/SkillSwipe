from sqlalchemy import Boolean, String, DateTime, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.core.enums import SourceType
from app.db.mixins import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from app.db.types import NAME_LENGTH, URL_LENGTH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.job import Job

class JobSource(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__= "job_sources"

    name: Mapped[str] = mapped_column(String(NAME_LENGTH), unique=True, nullable=False)

    base_url: Mapped[str] = mapped_column(String(URL_LENGTH), unique=True, nullable=False)
    last_scraped: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    status: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False, default=SourceType.SCRAPABLE)

    requests_per_minute: Mapped[int | None] = mapped_column(Integer, nullable=True)

    can_ban_scrappers: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


    jobs: Mapped[list["Job"]] = relationship(
        back_populates="source"
    )