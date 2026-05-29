from fastapi import Body, Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from auth.schemas import TokenPayload
from database.connection import get_db
from models import Employee
from employees.schemas import AddressCreate, EmployeeCreate, EmployeePatch, EmployeeResponse, GetEmployeeResponse
import employees.service as service


router = APIRouter(prefix="/employee", tags=["Employees"])
@router.post("", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(body: EmployeeCreate, db: AsyncSession = Depends(get_db), ):
    
    db_employee = await service.create(db, body=body)
    return db_employee

@router.get("", response_model=list[EmployeeResponse])
async def get_all_employees(db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)) -> list[Employee]:
    print("Current user:", _current_user)
    employees: Employee = await service.get_all_emp(db)

    return [emp for emp in employees]


@router.get("/{user_id}", response_model=GetEmployeeResponse)
async def get_employee(user_id: int, db: AsyncSession = Depends(get_db),):
    employee: Employee = await service.get_employee(db, user_id=user_id)

    return employee


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
async def patch_employee(user_id: int, body: EmployeePatch, db: AsyncSession = Depends(get_db)):
    id = user_id

    patched_employee: Employee = await service.patch_employee(db, id=id, body=body)

    return patched_employee


@router.delete("/{user_id}", response_model=EmployeeResponse)
async def delete_employee(user_id: int, db: AsyncSession = Depends(get_db),):
    deleted_employee: Employee = await service.delete_employee(db, user_id=user_id)

    return deleted_employee