from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from models import employee_departments
from models import employee
from models.employee import Employee
from exceptions import ConflictException, DBException, NotFoundException


async def create(db: AsyncSession, employee:Employee) -> Employee:
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


async def get_employee(db: AsyncSession, user_id: int) -> Employee:
    stmt = select(Employee).where(Employee.id == user_id)
    result = await db.scalars(stmt)

    return result.first()


async def patch_employee(db: AsyncSession, original_employee: Employee) -> Employee:
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise DBException(detail=f"Something went wrong: {str(e)}")
    
    await db.refresh(original_employee)

    return original_employee


async def delete_employee(db: AsyncSession, employee: Employee) -> Employee:
    employee.deleted_at = datetime.now()

    db.add(employee)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise DBException(detail=f"Something went wrong: {str(e)}")
    
    await db.refresh(employee)
    return employee


async def get_by_email(db: AsyncSession, email: str) -> Employee:
    stmt = select(Employee).where(
        Employee.email == email,
        Employee.deleted_at.is_(None)
    )

    res = await db.scalars(stmt)

    return res.first()

async def attach_department(db: AsyncSession, employee_id: int, department_id: int) -> None:
    try:
        await db.execute(
            employee_departments.insert().values(
                employee_id=employee_id,
                department_id=department_id,
            )
        )
        await db.commit()  

    except IntegrityError as e:
        await db.rollback()
        raise ConflictException(detail=f"Employee is already attached to department")
    

async def detach_department(db: AsyncSession, employee_id: int, department_id: int) -> None:
    try:
        await db.execute(
            employee_departments.delete().where(
                employee_departments.c.employee_id == employee_id,
                employee_departments.c.department_id == department_id
            )
        )
    except IntegrityError as e:
        await db.rollback()
        raise NotFoundException(detail="Employee id or department id not found")