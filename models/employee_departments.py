from sqlalchemy import Column, ForeignKey, Table

from models.entity import Entity


employee_departments = Table(
    "employee_departments",
    Entity.metadata,
    Column("employee_id", ForeignKey("employees.id"), primary_key=True),
    Column("department_id", ForeignKey("departments.id"), primary_key=True),
)
