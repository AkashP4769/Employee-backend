from sqlalchemy.ext.asyncio import AsyncSession

from department.schemas import DepartmentCreate, DepartmentPatch
from exceptions import NotFoundException
from models import Department
from department import repository


async def create(db: AsyncSession, body: DepartmentCreate) -> Department:
    department: Department = Department()
    department.name = body.name.strip()

    department = await repository.create(db, department=department)

    return department


async def get_all(db: AsyncSession) -> list[Department]:
    db_department = await repository.get_all(db)

    return db_department


async def get_by_id(db: AsyncSession, dept_id: int) -> Department:
    department: Department = await repository.get_by_id(db, dept_id=dept_id)

    if department is None:
        raise NotFoundException(detail=f"Department with id {dept_id} not found")

    return department


async def patch(db: AsyncSession, id: int, body: DepartmentPatch) -> Department:
    department: Department = await repository.get_by_id(db, dept_id=id)

    if department is None:
        raise NotFoundException(detail=f"Department with id {id} not found")

    if body.name is not None:
        department.name = body.name

    patched_department: Department = await repository.patch(db, department)

    return patched_department


async def delete(db: AsyncSession, dept_id: int) -> Department:
    department: Department = await repository.get_by_id(db, dept_id=dept_id)

    if department is None or department.deleted_at is not None:
        raise NotFoundException(detail=f"Department with id {dept_id} not found")

    deleted_department: Department = await repository.delete(db, department=department)

    return deleted_department
