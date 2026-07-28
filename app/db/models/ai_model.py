from sqlalchemy import String, Integer, Boolean, Enum, Numeric, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ModelProviders
from app.db.mixins import UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.db.base import Base
from app.db.types import NAME_LENGTH, URL_LENGTH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.ai_report import AIReport

class AIModel(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__= "ai_models"

    __table_args__= (
        UniqueConstraint(
            "provider",
            "model_name",
            "version",
            name="uq_ai_model"
        ),
        CheckConstraint(
            "context_window > 0",
            name="ck_ai_model_context_window"
        ),
        CheckConstraint(
            "input_cost_per_1m >= 0",
            name="ck_ai_model_input_cost",
        ),
        CheckConstraint(
            "output_cost_per_1m >= 0",
            name="ck_ai_model_output_cost",
        ),
    )

    model_name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    provider: Mapped[ModelProviders] = mapped_column(Enum(ModelProviders), nullable=False)

    version: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(URL_LENGTH), nullable=False)
    context_window: Mapped[int] = mapped_column(Integer, nullable=False)

    supports_streaming: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    supports_tools: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    input_cost_per_1m: Mapped[int] = mapped_column(Numeric, nullable=False)
    output_cost_per_1m: Mapped[int] = mapped_column(Numeric, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


    ai_reports: Mapped[list["AIReport"]] = relationship(
        back_populates="ai_model"
    )