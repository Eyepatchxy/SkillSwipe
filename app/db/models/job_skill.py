from sqlalchemy import Enum, ForeignKey, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid

from app.core.enums import SkillImportance
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.job import Job
    from app.db.models.skill import Skill

class JobSkill(Base):
    __tablename__="job_skills"

    __table_args__= (
        UniqueConstraint(
            "job_id",
            "skill_id",
            name="uq_job_skill",
        ),
    )

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("jobs.id", ondelete="CASCADE"), 
        nullable=False,
        primary_key=True,
        index=True
    )

    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("skills.id", ondelete="RESTRICT",), 
        nullable=False,
        primary_key=True,
        index=True
    )

    importance: Mapped[SkillImportance] = mapped_column(
        Enum(SkillImportance),
        nullable=False,
        default=SkillImportance.PREFERRED,
    )


    job: Mapped["Job"] = relationship(
        back_populates="job_skills"
    )
    skill: Mapped["Skill"] = relationship(
        back_populates="job_skills"
    )