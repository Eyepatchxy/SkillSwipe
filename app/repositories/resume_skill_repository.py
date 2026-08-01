"""Persistence operations for resume-to-skill associations."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.resume_skill import ResumeSkill
from app.repositories.base_repository import BaseRepository


class ResumeSkillRepository(BaseRepository[ResumeSkill]):
    """Persist and retrieve resume skill associations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ResumeSkill, session)

    async def get_resume_skills(self, resume_id: UUID) -> list[ResumeSkill]:
        """Return the skill associations for a resume."""
        result = await self.session.execute(select(ResumeSkill).where(ResumeSkill.resume_id == resume_id))
        return list(result.scalars())

    async def add_skill(self, resume_id: UUID, skill_id: UUID) -> ResumeSkill:
        """Add a skill association to the current unit of work."""
        resume_skill = ResumeSkill(resume_id=resume_id, skill_id=skill_id)
        self.session.add(resume_skill)
        return resume_skill

    async def remove_skill(self, resume_id: UUID, skill_id: UUID) -> bool:
        """Remove a skill association and report whether it existed."""
        result = await self.session.execute(
            delete(ResumeSkill).where(ResumeSkill.resume_id == resume_id, ResumeSkill.skill_id == skill_id)
        )
        return bool(result.rowcount)
