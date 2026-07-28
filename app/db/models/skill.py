from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import SkillCategory
from app.db.mixins import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from app.db.types import NAME_LENGTH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.job_skill import JobSkill
    from app.db.models.resume_skill import ResumeSkill

class Skill(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__= "skills"

    name: Mapped[str] = mapped_column(String(NAME_LENGTH), unique=True, nullable=False)

    category: Mapped[SkillCategory] = mapped_column(Enum(SkillCategory) , nullable=False)


    job_skills: Mapped[list["JobSkill"]] = relationship(
        back_populates="skill"
    )
    resume_skills: Mapped[list["ResumeSkill"]] = relationship(
        back_populates="skill"
    )