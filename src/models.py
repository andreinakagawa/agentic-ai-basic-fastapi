"""Global database models.

This file contains database models that are shared across the application.
Agent-specific models should be defined in their respective agent folders.

Examples of global models:
- User
- APIKey
- AuditLog
- SystemConfiguration
"""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class BaseModel(Base):
    """Base model with common fields for all models."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


# Example: Global model for API keys (if needed)
# class APIKey(BaseModel):
#     __tablename__ = "api_keys"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


# Add more global models as needed
