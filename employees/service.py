from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from employees.schemas import EmployeeCreate, EmployeePatch
from exceptions import *
from models.employee import Employee
import employees.repository as repository
from auth.utils import hash_password, verify_password, create_access_token


async def create(db: AsyncSession, body: EmployeeCreate) -> Employee:
    employee: Employee = Employee()

    employee.name = body.name.strip()
    employee.email = body.email.strip()
    employee.password_hash = hash_password(body.password)
    employee.age = body.age

    if not isinstance(employee.name, str) or not employee.name:
        raise BadRequestException(detail="email must be a non-empty string")
    if not isinstance(employee.email, str) or not employee.email:
        raise BadRequestException(detail="email must be a non-empty string")
    
    employee = await repository.create(db, employee=employee)

    return employee


async def get_all_emp(db: AsyncSession) -> list[Employee]:
    db_employees = await repository.get_all(db)

    return db_employees


async def get_employee(db: AsyncSession, user_id: int) -> Employee:
    employee: Employee = await repository.get_employee(db, user_id=user_id)

    if employee is None:
        raise NotFoundException(detail="User not found")
    
    return employee


async def patch_employee(db: AsyncSession, id: int, body: EmployeePatch) -> Employee:
    original_employee: Employee = await repository.get_employee(db, user_id=id)

    if original_employee is None:
        raise NotFoundException(detail="User not found")
    
    if body.name is not None:
        original_employee.name = body.name

    if body.email is not None:
        original_employee.email = body.email
    
    patched_employee: Employee = await repository.patch_employee(db, original_employee)

    return patched_employee


async def delete_employee(db: AsyncSession, user_id: int) -> Employee:
    employee: Employee = await repository.get_employee(db, user_id=user_id)

    if employee is None or employee.deleted_at is not None:
        raise NotFoundException(detail="User not found")
    
    deleted_employee: Employee = await repository.delete_employee(db, employee=employee)

    return deleted_employee
    
async def login(db: AsyncSession, email: str, password: str) -> str:
    employee: Employee = await repository.get_by_email(email=email)

    if employee is None:
        raise UnauthorizedException("Invalid username or password")
    
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid username or password")
    
    return create_access_token({"id": employee.id, "email": employee.email})
