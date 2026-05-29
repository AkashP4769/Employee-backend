from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.employee import Employee
import employees.repository as repository


async def create(db: AsyncSession, employee: Employee) -> Employee:

    employee.name = employee.name.strip()
    employee.email = employee.email.strip()

    if not isinstance(employee.name, str) or not employee.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
    if not isinstance(employee.email, str) or not employee.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
    
    
    employee = await repository.create(db, employee=employee)

    return employee


async def get_all_emp(db: AsyncSession) -> list[Employee]:
    db_employees = await repository.get_all(db)

    return db_employees


async def get_employee(db: AsyncSession, user_id: int) -> Employee:
    employee: Employee = await repository.get_employee(db, user_id=user_id)

    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return employee


async def patch_employee(db: AsyncSession, employee: Employee) -> Employee:
    original_employee: Employee = await repository.get_employee(db, user_id=employee.id)

    if original_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    patched_employee: Employee = await repository.patch_employee(db, original_employee, employee)

    return patched_employee


async def delete_employee(db: AsyncSession, user_id: int) -> Employee:
    employee: Employee = await repository.get_employee(db, user_id=user_id)

    if employee is None or employee.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    deleted_employee: Employee = await repository.delete_employee(db, employee=employee)

    return deleted_employee
    
