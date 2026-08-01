"""Persistence operations for notifications."""

from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.notification import Notification
from app.repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    """Persist and retrieve notification records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Notification, session)

    async def user_notifications(self, user_id: UUID) -> list[Notification]:
        """Return a user's notifications, newest first."""
        result = await self.session.execute(
            select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc())
        )
        return list(result.scalars())

    async def unread(self, user_id: UUID) -> list[Notification]:
        """Return unread notifications for a user, newest first."""
        result = await self.session.execute(
            select(Notification)
            .where(Notification.user_id == user_id, Notification.is_read.is_(False))
            .order_by(Notification.created_at.desc())
        )
        return list(result.scalars())

    async def mark_read(self, notification: Notification) -> Notification:
        """Mark a notification as read in the current unit of work."""
        notification.is_read = True
        return notification

    async def delete_old_notifications(self, older_than: datetime | None = None) -> list[Notification]:
        """Delete notifications older than the supplied cutoff or 30 days."""
        cutoff = older_than or datetime.now(timezone.utc) - timedelta(days=30)
        result = await self.session.execute(select(Notification).where(Notification.created_at < cutoff))
        notifications = list(result.scalars())
        for notification in notifications:
            await self.session.delete(notification)
        return notifications
