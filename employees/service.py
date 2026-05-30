from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from employees.schemas import EmployeeCreate, EmployeeDepartmentResponse, EmployeePatch
from exceptions import *
from models.address import Address
from models.employee import Employee
from models.department import Department
import employees.repository as repository
from auth.utils import hash_password
from department import service as department_service

async def create(db: AsyncSession, body: EmployeeCreate) -> Employee:
    employee: Employee = Employee()

    employee.name = body.name.strip()
    employee.email = body.email.strip()
    employee.password_hash = hash_password(body.password)
    employee.age = body.age

    if body.address is not None:
        address = Address(**body.address.model_dump())
        employee.addresses.append(address)
    
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
    # TODO: Remove repo calls in service layer

    employee: Employee = await repository.get_employee(db, user_id=user_id)

    if employee is None or employee.deleted_at is not None:
        raise NotFoundException(detail="User not found")
    
    deleted_employee: Employee = await repository.delete_employee(db, employee=employee)

    return deleted_employee


async def attach_department(db: AsyncSession, employee_id: int, department_id: int) -> dict:
    employee = await repository.get_employee(db, user_id=employee_id)
    department = await department_service.get_by_id(db, dept_id=department_id)

    if not employee:
        raise NotFoundException(detail="Employee not found")
    if not department:
        raise NotFoundException(detail="Department not found")

    await repository.attach_department(db, employee_id=employee_id, department_id=department_id)

    return {
        "employee_id": employee_id,
        "department_id": department_id
    }
    
async def detach_department(db: AsyncSession, employee_id: int, department_id: int) -> dict:
    await repository.detach_department(db, employee_id=employee_id, department_id=department_id)

    return {
        "employee_id": employee_id,
        "department_id": department_id
    }
    
