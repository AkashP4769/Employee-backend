from fastapi import HTTPException, status
from sqlalchemy import Sequence, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from models.employee import Employee


async def create(db: AsyncSession, employee:Employee) -> Employee:
    db.add(employee)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{employee.email}' is already in use")
    
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


async def patch_employee(db: AsyncSession, original_employee: Employee, new_employee: Employee) -> Employee:
    if new_employee.name is not None:
        original_employee.name = new_employee.name

    if new_employee.email is not None:
        original_employee.email = new_employee.email

    # db.add(original_employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Integrity Error")
    
    await db.refresh(original_employee)

    return original_employee


async def delete_employee(db: AsyncSession, employee: Employee) -> Employee:
    employee.deleted_at = datetime.now()

    db.add(employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Integrity Error")
    
    await db.refresh(employee)
    return employee