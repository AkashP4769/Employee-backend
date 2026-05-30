"""
Employee entity — ORM mapped class for table `employees`.
"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Entity, employee_departments


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


class Employee(Entity):
    __abstract__ = False
    __tablename__ = "employees"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)

    password_hash: Mapped[int] = mapped_column(String(255), nullable=False)

    addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="employee",
        cascade="all, delete-orphan"
    )

    departments: Mapped[list["Department"]] = relationship(
        secondary="employee_departments",
        back_populates="employees"
    )

    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "created_at": _datetime_to_iso(self.created_at),
            "updated_at": _datetime_to_iso(self.updated_at),
            "deleted_at": _datetime_to_iso(self.deleted_at),
        }
    
    def __repr__(self):
        return f"Employee(id: {self.id}, name: {self.name}, email: {self.email}, age: {self.age})"