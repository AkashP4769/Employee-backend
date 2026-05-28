from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uvicorn
import logging

from database.connection import create_tables, get_db
from middleware.logger import RequestLoggingMiddleware
from models.employee import Employee


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="Employee App",
    description="A simple employee management application",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
)


@app.get("/employee", tags=["Employees"])
async def get_all_employees(db: AsyncSession = Depends(get_db), ):
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    result = await db.scalars(stmt)

    return [r.to_api_dict() for r in result.all()]

@app.post("/employee", status_code=status.HTTP_201_CREATED, tags=["Employees"])
async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    name = body.get("name")
    email = body.get("email")

    if not isinstance(name, str) or not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
    
    db_employee = Employee(name=name.strip(), email=email.strip())
    db.add(db_employee)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
    
    await db.refresh(db_employee)
    return db_employee.to_api_dict()

@app.get("/employee/{user_id}", tags=["Employees"])
async def get_employee(user_id: int, db: AsyncSession = Depends(get_db), ):
    stmt = select(Employee).where(Employee.id == user_id)
    result = await db.scalars(stmt)

    emp = result.first()
    if emp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result.first().to_api_dict()

@app.patch("/employee", status_code=status.HTTP_200_OK, tags=["Employees"])
async def patch_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    id = body.get("id", None)
    name = body.get("name", None)
    email = body.get("email", None)

    stmt = select(Employee).where(Employee.id == id)
    result = await db.scalars(stmt)

    emp = result.first()

    if emp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if name is not None:
        emp.name = name

    if email is not None:
        emp.email = email

    db.add(emp)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Integrity Error")
    
    await db.refresh(emp)
    return emp.to_api_dict()


@app.delete("/employee/{user_id}", tags=["Employees"])
async def delete_employee(user_id: int, db: AsyncSession = Depends(get_db), ):
    stmt = select(Employee).where(Employee.id == user_id)
    result = await db.scalars(stmt)

    emp = result.first()
    if emp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    emp.deleted_at = datetime.now()

    db.add(emp)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Integrity Error")
    
    await db.refresh(emp)
    return emp.to_api_dict()



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)