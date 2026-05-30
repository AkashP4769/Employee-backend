

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class DepartmentCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)

class DepartmentPatch(BaseModel):
    name: str = Field(min_length=3, max_length=100, default=None)

class DepartmentResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class GetDepartmentResponse(DepartmentResponse):
    created_at: datetime
    updated_at: datetime