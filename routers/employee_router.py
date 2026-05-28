from fastapi import Body, Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from models.employee import Employee
import services.employee_service as employee_service


router = APIRouter(prefix="/employee", tags=["Employees"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    name = body.get("name")
    email = body.get("email")
    employee = Employee(name=name, email=email)

    db_employee = await employee_service.create(db, employee=employee)
    return db_employee.to_api_dict()


@router.get("", response_model=None)
async def get_all_employees(db: AsyncSession = Depends(get_db)) -> list[Employee]:
    employees = await employee_service.get_all_emp(db)

    return [emp.to_api_dict() for emp in employees]


@router.get("/{user_id}",)
async def get_employee(user_id: int, db: AsyncSession = Depends(get_db),):
    employee: Employee = await employee_service.get_employee(db, user_id=user_id)

    return employee.to_api_dict()


@router.patch("", status_code=status.HTTP_200_OK,)
async def patch_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    id = body.get("id", None)
    name = body.get("name", None)
    email = body.get("email", None)

    employee: Employee = Employee(id=id, name=name, email=email)

    patched_employee: Employee = await employee_service.patch_employee(db, employee=employee)

    return patched_employee.to_api_dict()


@router.delete("/{user_id}",)
async def delete_employee(user_id: int, db: AsyncSession = Depends(get_db),):
    deleted_employee: Employee = await employee_service.delete_employee(db, user_id=user_id)

    return deleted_employee.to_api_dict()