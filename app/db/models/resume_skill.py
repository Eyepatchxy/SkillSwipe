from sqlalchemy import Enum, ForeignKey, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from app.core.enums import SkillProficiency
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.resume import Resume
    from app.db.models.skill import Skill

class ResumeSkill(Base):
    __tablename__="resume_skills"

    __table_args__= (
        UniqueConstraint(
            "resume_id",
            "skill_id",
            name="uq_resume_skill"
        ),
    )

    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("resumes.id", ondelete="CASCADE"), 
        nullable=False,
        primary_key=True,
        index=True
    )

    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("skills.id", ondelete="RESTRICT"), 
        nullable=False,
        primary_key=True,
        index=True
    )

    confidence: Mapped[SkillProficiency] = mapped_column(
        Enum(SkillProficiency),
        nullable=False,
        default=SkillProficiency.BEGINNER,
    )


    resume: Mapped["Resume"] = relationship(
        back_populates="resume_skills"
    )
    skill: Mapped["Skill"] = relationship(
        back_populates="resume_skills"
    )