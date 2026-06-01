from fastapi import Body, Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from auth.schemas import TokenPayload
from database.connection import get_db
from models import Employee
from employees.schemas import AddressResponse, EmployeeCreate, EmployeePatch, EmployeeResponse, GetEmployeeResponse 
from employees.schemas import EmployeeDepartmentResponse
import employees.service as service


router = APIRouter(prefix="/employee", tags=["Employees"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(body: EmployeeCreate, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user) ):
    db_employee = await service.create(db, body=body)
    return db_employee


@router.get("", response_model=list[EmployeeResponse])
async def get_all_employees(db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)) -> list[Employee]:
    employees: Employee = await service.get_all_emp(db)

    return [emp for emp in employees]


@router.get("/{employee_id}", response_model=GetEmployeeResponse)
async def get_employee(employee_id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    employee: Employee = await service.get_employee(db, employee_id=employee_id)

    return employee


@router.patch("/{employee_id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
async def patch_employee(employee_id: int, body: EmployeePatch, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    id = employee_id

    patched_employee: Employee = await service.patch_employee(db, id=id, body=body)

    return patched_employee


@router.delete("/{employee_id}", response_model=EmployeeResponse)
async def delete_employee(employee_id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    deleted_employee: Employee = await service.delete_employee(db, employee_id=employee_id)

    return deleted_employee


@router.post('/{employee_id}/departments/{department_id}', response_model=EmployeeDepartmentResponse)
async def attach_employee_to_department(employee_id: int, department_id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    attached_employee = await service.attach_department(db, employee_id, department_id)

    return attached_employee

@router.delete('/{employee_id}/departments/{department_id}', response_model=EmployeeDepartmentResponse)
async def detach_employee_to_department(employee_id: int, department_id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    detached_employee = await service.detach_department(db, employee_id, department_id)

    return detached_employee

@router.post('/{employee_id}/addresses', response_model=AddressResponse)
async def add_employee_address(employee_id: int, body: AddressResponse, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    added_address = await service.add_address(db, employee_id, body)

    return added_address

@router.delete('/{employee_id}/addresses/{address_id}', response_model=AddressResponse)
async def delete_employee_address(employee_id: int, addess_id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    deleted_address = await service.delete_address(db, employee_id, addess_id)

    return deleted_address

@router.get('/{employee_id}/addresses', response_model=list[AddressResponse])
async def get_employee_addresses(employee_id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)  ):
    addresses = await service.get_addresses(db, employee_id)

    return addresses