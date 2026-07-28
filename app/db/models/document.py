from sqlalchemy import String, Enum, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from app.core.enums import MimeType, StorageProvider
from app.db.mixins import UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from app.db.types import NAME_LENGTH, CHECKSUM_LENGTH, STORAGE_KEY_LENGTH

from typing import TYPE_CHECKING

if TYPE_CHECKING:    
    from app.db.models.user import User
    from app.db.models.resume import Resume
    from app.db.models.certification import Certification
    from app.db.models.cover_letter import CoverLetter


class Document(UUIDMixin, UserOwnedMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "documents"

    storage_provider: Mapped[StorageProvider] = mapped_column(Enum(StorageProvider), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(STORAGE_KEY_LENGTH), nullable=False)

    original_filename: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)

    mime_type: Mapped[MimeType] = mapped_column(Enum(MimeType), nullable=False)

    file_size: Mapped[int] = mapped_column(nullable=False)

    checksum: Mapped[str] = mapped_column(String(CHECKSUM_LENGTH), unique=True, nullable=False) #Index



    user: Mapped["User"] = relationship(
        back_populates="documents"
    )
    resume: Mapped["Resume"] = relationship(
        back_populates="document"
    )
    certification: Mapped["Certification"] = relationship(
        back_populates="document"
    )
    cover_letter: Mapped["CoverLetter"] = relationship(
        back_populates="document"
    )