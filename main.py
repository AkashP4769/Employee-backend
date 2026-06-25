from fastapi import FastAPI
import uvicorn
import logging

from middleware import configure_middleware
from employees.router import router as employee_router
from auth.router import router as auth_router
from department.router import router as department_router
from agent.router import router as agent_router
from config import setting
from exceptions.handler import register_exception_handlers


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


app = FastAPI(
    title="Employee App",
    description="A simple employee management application",
    version="1.0.0",
)

configure_middleware(app)
register_exception_handlers(app)
app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(department_router)
app.include_router(agent_router)


@app.get("/health", tags=["health"], status_code=200)
def health():
    return {
        "message": f"App is healthy. Environment: {setting.app_env}",
        "status": "healthy",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)
