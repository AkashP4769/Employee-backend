from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from auth.schemas import TokenPayload
from database.connection import get_db
from models import Department
from department.schemas import (
    DepartmentCreate,
    DepartmentPatch,
    DepartmentResponse,
    GetDepartmentResponse,
)
import department.service as service


router = APIRouter(prefix="/department", tags=["department"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=DepartmentResponse)
async def create_department(
    body: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    db_department = await service.create(db, body=body)
    return db_department


@router.get("", response_model=list[DepartmentResponse])
async def get_all_department(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
) -> list[DepartmentResponse]:
    department: Department = await service.get_all(db)

    return [dept for dept in department]


@router.get("/{dept_id}", response_model=GetDepartmentResponse)
async def get_department(
    dept_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    department: Department = await service.get_by_id(db, dept_id=dept_id)

    return department


@router.patch(
    "/{dept_id}", status_code=status.HTTP_200_OK, response_model=DepartmentResponse
)
async def patch_department(
    dept_id: int,
    body: DepartmentPatch,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    id = dept_id
    patched_department: Department = await service.patch(db, id=id, body=body)

    return patched_department


@router.delete("/{dept_id}", response_model=DepartmentResponse)
async def delete_department(
    dept_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    deleted_department: Department = await service.delete(db, dept_id=dept_id)

    return deleted_department
