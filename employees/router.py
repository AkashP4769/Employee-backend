from fastapi import Body, Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from models import Employee
from employees.schemas import AddressCreate, EmployeeCreate, EmployeeResponse, GetEmployeeResponse
import employees.service as service


router = APIRouter(prefix="/employee", tags=["Employees"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(body: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    employee = Employee(name=body.name, email=body.email, age=body.age)

    db_employee = await service.create(db, employee=employee)
    return db_employee


@router.get("", response_model=list[EmployeeResponse])
async def get_all_employees(db: AsyncSession = Depends(get_db)) -> list[Employee]:
    employees: Employee = await service.get_all_emp(db)

    return [emp for emp in employees]


@router.get("/{user_id}", response_model=GetEmployeeResponse)
async def get_employee(user_id: int, db: AsyncSession = Depends(get_db),):
    employee: Employee = await service.get_employee(db, user_id=user_id)

    return employee


@router.patch("", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
async def patch_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    id = body.get("id", None)
    name = body.get("name", None)
    email = body.get("email", None)
    employee: Employee = Employee(id=id, name=name, email=email)

    patched_employee: Employee = await service.patch_employee(db, employee=employee)

    return patched_employee


@router.delete("/{user_id}", response_model=EmployeeResponse)
async def delete_employee(user_id: int, db: AsyncSession = Depends(get_db),):
    deleted_employee: Employee = await service.delete_employee(db, user_id=user_id)

    return deleted_employee