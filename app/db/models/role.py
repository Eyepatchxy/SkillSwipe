from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.types import NAME_LENGTH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.preferred_role import PreferredRole

class Role(UUIDMixin, Base):
    __tablename__="roles"

    name: Mapped[str] = mapped_column(
        String(NAME_LENGTH),
        nullable=False,
        unique=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )


    preferred_roles: Mapped[list["PreferredRole"]] = relationship(
        back_populates="role"
    )