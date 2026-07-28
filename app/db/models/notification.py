from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import NotificationType
from app.db.base import Base
from app.db.mixins import UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin
from app.db.types import NAME_LENGTH, URL_LENGTH, DESCRIPTION_LENGTH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user import User

class Notification(UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__="notifications"

    title: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)

    message: Mapped[str] = mapped_column(String(DESCRIPTION_LENGTH), nullable=False)

    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType), 
        nullable=False
    )

    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)

    action_url: Mapped[str | None] = mapped_column(String(URL_LENGTH), nullable=True)


    user: Mapped["User"] = relationship(
        back_populates="notifications"
    )