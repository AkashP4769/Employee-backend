# return {
#             "id": self.id,
#             "name": self.name,
#             "created_at": datetime_to_iso(self.created_at),
#             "updated_at": datetime_to_iso(self.updated_at),
#             "deleted_at": datetime_to_iso(self.deleted_at),
#         }

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Entity

class Department(Entity):
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    employees: Mapped["employees"] = relationship("Employee", back_populates="employees")