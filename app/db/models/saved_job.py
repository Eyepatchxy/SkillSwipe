from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from app.db.mixins import TimestampMixin
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user import User

class SavedJob(TimestampMixin, Base):
    __tablename__="saved_jobs"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True
    )

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        primary_key=True,
        index=True
    )


    user: Mapped["User"] = relationship(
        back_populates="saved_jobs"
    )