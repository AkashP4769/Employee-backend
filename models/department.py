from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Entity, employee_departments

class Department(Entity):
    __tablename__ = "departments"
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    employees: Mapped[list["Employee"]] = relationship(
        secondary=employee_departments,
        back_populates="departments"
    )


