from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
import logging

from middleware import configure_middleware
from database.connection import create_tables
from routers.employee_router import router as employee_router
from config import APP_ENV


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


app = FastAPI(
    title="Employee App",
    description="A simple employee management application",
    version="1.0.0",
)

configure_middleware(app)
app.include_router(employee_router)

@app.get("/health", tags=["health"])
def health():
    return {"message": f"App is healthy. Environment: {APP_ENV}"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)