
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils import verify_password, create_access_token
from employees import repository
from exceptions import UnauthorizedException
from models.employee import Employee

async def login(db: AsyncSession, email: str, password: str) -> str:
    employee: Employee = await repository.get_by_email(db, email=email)

    if employee is None:
        raise UnauthorizedException("Invalid username or password")
    
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid username or password")
    
    return create_access_token({"id": employee.id, "email": employee.email})
