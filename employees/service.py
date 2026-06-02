from sqlalchemy.ext.asyncio import AsyncSession

from employees.schemas import AddressResponse, EmployeeCreate, EmployeePatch
from exceptions import NotFoundException, ConflictException
from models.address import Address
from models.employee import Employee
import employees.repository as repository
from auth.utils import hash_password
from department import service as department_service


async def create(db: AsyncSession, body: EmployeeCreate) -> Employee:
    employee: Employee = Employee()

    employee.name = body.name.strip()
    employee.email = body.email.strip()
    employee.password_hash = hash_password(body.password)
    employee.age = body.age
    employee.role = body.role

    if body.address is not None:
        address = Address(**body.address.model_dump())
        employee.addresses.append(address)

    employee = await repository.create(db, employee=employee)

    return employee


async def get_all_emp(db: AsyncSession) -> list[Employee]:
    db_employees = await repository.get_all(db)

    return db_employees


async def get_employee(db: AsyncSession, employee_id: int) -> Employee:
    employee: Employee = await repository.get_employee_by_id(
        db, employee_id=employee_id
    )

    if employee is None:
        raise NotFoundException(detail=f"Employee with id {employee_id} not found")

    return employee


async def patch_employee(db: AsyncSession, id: int, body: EmployeePatch) -> Employee:
    employee: Employee = await repository.get_employee_by_id(db, employee_id=id)

    if employee is None:
        raise NotFoundException(detail=f"Employee with id {id} not found")

    if body.name is not None:
        employee.name = body.name

    if body.email is not None:
        employee.email = body.email

    if body.password is not None:
        employee.password_hash = hash_password(body.password)

    if body.age is not None:
        employee.age = body.age

    if body.role is not None:
        employee.role = body.role

    patched_employee: Employee = await repository.patch_employee(db, employee)

    return patched_employee


async def delete_employee(db: AsyncSession, employee_id: int) -> Employee:
    employee: Employee = await repository.get_employee_by_id(
        db, employee_id=employee_id
    )

    if employee is None or employee.deleted_at is not None:
        raise NotFoundException(detail=f"Employee with id {employee_id} not found")

    deleted_employee: Employee = await repository.delete_employee(db, employee=employee)

    return deleted_employee


async def attach_department(
    db: AsyncSession, employee_id: int, department_id: int
) -> dict:
    employee = await repository.get_employee_by_id(db, employee_id=employee_id)
    department = await department_service.get_by_id(db, dept_id=department_id)

    if not employee or employee.deleted_at is not None:
        raise NotFoundException(detail=f"Employee with id {employee_id} not found")
    if not department or department.deleted_at is not None:
        raise NotFoundException(detail=f"Department with id {department_id} not found")

    await repository.attach_department(
        db, employee_id=employee_id, department_id=department_id
    )

    return {"employee_id": employee_id, "department_id": department_id}


async def detach_department(
    db: AsyncSession, employee_id: int, department_id: int
) -> dict:
    await repository.detach_department(
        db, employee_id=employee_id, department_id=department_id
    )

    return {"employee_id": employee_id, "department_id": department_id}


async def delete_address(
    db: AsyncSession, employee_id: int, address_id: int
) -> Address:
    address: Address = await repository.get_address_by_id(db, address_id)

    if not address:
        raise NotFoundException(f"Address with id {address_id} not found")

    if address.employee_id != employee_id:
        raise ConflictException(f"Address doesn't belong to employee {employee_id}")

    deleted_address = await repository.delete_address(db, address=address)

    return deleted_address


async def add_address(
    db: AsyncSession, employee_id: int, body: AddressResponse
) -> Address:
    employee = await repository.get_employee_by_id(db, employee_id=employee_id)

    if not employee:
        raise NotFoundException(f"Employee {employee_id} not found")

    address = Address(**body.model_dump())
    address.employee_id = employee_id

    added_address = await repository.add_address(
        db, employee_id=employee_id, address=address
    )

    return added_address


async def get_addresses(db: AsyncSession, employee_id: int) -> list[Address]:
    employee = await repository.get_employee_by_id(db, employee_id=employee_id)

    if not employee:
        raise NotFoundException(f"Employee with id {employee_id} not found")

    addresses = await repository.get_addresses_by_employee_id(
        db, employee_id=employee_id
    )

    return addresses
