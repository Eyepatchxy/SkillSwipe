from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.types import NAME_LENGTH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.company import Company
    from app.db.models.preferred_location import PreferredLocation

class Location(UUIDMixin, Base):
    __tablename__="locations"

    name: Mapped[str] = mapped_column(
        String(NAME_LENGTH),
        nullable=False,
        unique=True
    )


    companies: Mapped[list["Company"]] = relationship(
        back_populates="location"
    )
    preferred_locations: Mapped[list["PreferredLocation"]] = relationship(
        back_populates="location"
    )