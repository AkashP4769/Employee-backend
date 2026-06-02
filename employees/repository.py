from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from models import employee_departments
from models.address import Address
from models.employee import Employee
from exceptions import ConflictException, DBException, NotFoundException


async def create(db: AsyncSession, employee: Employee) -> Employee:
    db.add(employee)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(detail=f"Email '{employee.email}' is already in use")

    await db.refresh(employee)
    return employee


async def get_all(db: AsyncSession) -> list[Employee]:
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    result = await db.scalars(stmt)

    return result.all()


async def get_employee(db: AsyncSession, employee_id: int) -> Employee:
    stmt = select(Employee).where(Employee.id == employee_id)
    result = await db.scalars(stmt)

    return result.first()


async def patch_employee(db: AsyncSession, original_employee: Employee) -> Employee:
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise DBException(
            detail=f"Error during patching of employee of id {original_employee.id} in db"
        )

    await db.refresh(original_employee)

    return original_employee


async def delete_employee(db: AsyncSession, employee: Employee) -> Employee:
    employee.deleted_at = datetime.now()

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise DBException(
            detail=f"Error during deletion of employee of id {employee.id} in db"
        )

    await db.refresh(employee)
    return employee


async def get_by_email(db: AsyncSession, email: str) -> Employee:
    stmt = select(Employee).where(
        Employee.email == email, Employee.deleted_at.is_(None)
    )

    res = await db.scalars(stmt)

    return res.first()


async def attach_department(
    db: AsyncSession, employee_id: int, department_id: int
) -> None:
    try:
        await db.execute(
            employee_departments.insert().values(
                employee_id=employee_id,
                department_id=department_id,
            )
        )
        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise ConflictException(
            detail=f"Employee {employee_id} is already attached to department {department_id}"
        )


async def detach_department(
    db: AsyncSession, employee_id: int, department_id: int
) -> None:
    try:
        await db.execute(
            employee_departments.delete().where(
                employee_departments.c.employee_id == employee_id,
                employee_departments.c.department_id == department_id,
            )
        )

        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise NotFoundException(
            detail=f"Employee id {employee_id} or department id {department_id} not found"
        )


async def delete_address(db: AsyncSession, address: Address) -> Address:
    address.deleted_at = datetime.now()

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise DBException(detail=f"Error while deleting address {address.id}")

    await db.refresh(address)
    return address


async def get_address_by_id(db: AsyncSession, address_id: int) -> Address:
    stmt = select(Address).where(Address.id == address_id, Address.deleted_at.is_(None))

    res = await db.scalars(stmt)

    return res.first()


async def add_address(db: AsyncSession, employee_id: int, address: Address) -> Address:
    db.add(address)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise DBException(
            detail=f"Error while adding address for employee {employee_id}"
        )

    await db.refresh(address)
    return address


async def get_addresses_by_employee_id(
    db: AsyncSession, employee_id: int
) -> list[Address]:
    stmt = select(Address).where(
        Address.employee_id == employee_id, Address.deleted_at.is_(None)
    )

    res = await db.scalars(stmt)

    return res.all()
