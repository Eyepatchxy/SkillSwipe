from sqlalchemy import Enum, UUID, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

import uuid

from app.core.enums import ActivityAction, EntityType
from app.db.base import Base
from app.db.mixins import UUIDMixin, TimestampMixin
from app.db.types import IP_ADDRESS_LENGTH, USER_AGENT_LENGTH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user import User

class ActivityLog(UUIDMixin, TimestampMixin, Base):
    __tablename__="activity_logs"

    user_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True
    )

    action: Mapped[ActivityAction] = mapped_column(
        Enum(ActivityAction),
        nullable=False,
        index=True
    )

    entity_type: Mapped[EntityType] = mapped_column(
        Enum(EntityType),
        nullable=False
    )

    entity_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True
    )

    payload: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(IP_ADDRESS_LENGTH), 
        nullable=True
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(USER_AGENT_LENGTH), 
        nullable=True
    )


    user: Mapped["User"] = relationship(
        back_populates="activity_logs"
    )