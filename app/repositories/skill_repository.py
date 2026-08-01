"""Persistence operations for skills."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.resume_skill import ResumeSkill
from app.db.models.skill import Skill
from app.repositories.base_repository import BaseRepository


class SkillRepository(BaseRepository[Skill]):
    """Persist and retrieve skill records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Skill, session)

    async def get_by_name(self, name: str) -> Skill | None:
        """Return a skill by case-insensitive exact name."""
        result = await self.session.execute(select(Skill).where(func.lower(Skill.name) == name.lower()))
        return result.scalar_one_or_none()

    async def search(self, name: str) -> list[Skill]:
        """Return skills whose names contain ``name``."""
        result = await self.session.execute(select(Skill).where(Skill.name.ilike(f"%{name.strip()}%")).order_by(Skill.name))
        return list(result.scalars())

    async def popular(self, limit: int) -> list[Skill]:
        """Return the most frequently used resume skills."""
        statement = (
            select(Skill)
            .outerjoin(ResumeSkill, ResumeSkill.skill_id == Skill.id)
            .group_by(Skill.id)
            .order_by(func.count(ResumeSkill.skill_id).desc(), Skill.name)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return list(result.scalars())
