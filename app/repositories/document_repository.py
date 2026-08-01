"""Persistence operations for documents."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document import Document
from app.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """Persist and retrieve document records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Document, session)

    async def get_by_storage_key(self, key: str) -> Document | None:
        """Return the document stored under ``key``, if present."""
        result = await self.session.execute(select(Document).where(Document.storage_key == key))
        return result.scalar_one_or_none()

    async def get_user_documents(self, user_id: UUID) -> list[Document]:
        """Return a user's documents, newest first."""
        result = await self.session.execute(
            select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc())
        )
        return list(result.scalars())

    async def delete_orphan_documents(self) -> list[Document]:
        """Delete documents not referenced by a resume, certification, or cover letter."""
        statement = select(Document).where(
            ~Document.resume.has(),
            ~Document.certification.has(),
            ~Document.cover_letter.has(),
        )
        result = await self.session.execute(statement)
        documents = list(result.scalars())
        for document in documents:
            await self.session.delete(document)
        return documents
