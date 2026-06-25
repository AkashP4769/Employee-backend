from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Entity


class Department(Entity):
    __tablename__ = "departments"
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    employees: Mapped[list["Employee"]] = relationship(  # noqa: F821
        secondary="employee_departments", back_populates="departments"
    )

    def __repr__(self) -> str:
        return f"Department(id={self.id}, name={self.name})"
