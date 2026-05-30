from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from models import Department
from exceptions import DBException

async def create(db: AsyncSession, department:Department) -> Department:
    db.add(department)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise DBException(detail="Error during dept creation in db")
    
    await db.refresh(department)
    return department


async def get_all(db: AsyncSession) -> list[Department]:
    stmt = select(Department).where(Department.deleted_at.is_(None))
    result = await db.scalars(stmt)

    return result.all()


async def get_by_id(db: AsyncSession, dept_id: int) -> Department:
    stmt = select(Department).where(Department.id == dept_id)
    result = await db.scalars(stmt)

    return result.first()


async def patch(db: AsyncSession, department: Department) -> Department:
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise DBException(detail=f"Error during dept updating database: {str(e)}")
    
    await db.refresh(department)

    return department


async def delete(db: AsyncSession, department: Department) -> Department:
    department.deleted_at = datetime.now()

    db.add(department)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise DBException(detail=f"Error during dept deletion in db: {str(e)}")
    
    await db.refresh(department)
    return department
