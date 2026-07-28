from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import UUIDMixin
from app.db.types import NAME_LENGTH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.company import Company
    from app.db.models.preferred_industry import PreferredIndustry

class Industry(UUIDMixin, Base):
    __tablename__="industries"

    name: Mapped[str] = mapped_column(
        String(NAME_LENGTH),
        nullable=False,
        unique=True
    )

    companies: Mapped[list["Company"]] = relationship(
        back_populates="industry"
    )
    preferred_industries: Mapped[list["PreferredIndustry"]] = relationship(
        back_populates="industry"
    )