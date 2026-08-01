"""Persistence operations for users."""

from datetime import datetime
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import AccountStatus
from app.db.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Persist and retrieve :class:`User` instances."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        """Return the user with an email address, if present."""
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> User | None:
        """Return the user with a phone number, if present."""
        result = await self.session.execute(select(User).where(User.phone_number == phone))
        return result.scalar_one_or_none()

    async def search(self, query: str) -> list[User]:
        """Return users whose name or email contains the query."""
        pattern = f"%{query.strip()}%"
        statement = select(User).where(
            or_(User.first_name.ilike(pattern), User.last_name.ilike(pattern), User.email.ilike(pattern))
        ).order_by(User.first_name, User.last_name)
        result = await self.session.execute(statement)
        return list(result.scalars())

    async def get_active_users(self) -> list[User]:
        """Return users with an active account status."""
        result = await self.session.execute(select(User).where(User.account_status == AccountStatus.ACTIVE))
        return list(result.scalars())

    async def update_last_login(self, user: User) -> User:
        """Set a user's last-login timestamp in the current unit of work."""
        user.last_login = datetime.utcnow()
        return user
