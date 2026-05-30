from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic import field_validator, model_validator
from datetime import datetime

class AddressCreate(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

    @field_validator('postal_code')
    @classmethod
    def validate_psotal_code(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("postal_code value should be a digit (0-9)")
        
        return value
    
    @model_validator(mode='after')
    def postal_code_length_for_country(self):
        pincodes = {
            "US": 5,
            "IN": 6
        }

        pincode = pincodes.get(self.country, None)
        if pincode is None:
            raise ValueError("Not a valid country")
        
        if len(self.postal_code) != pincode:
            raise ValueError(f"Invalid postal code length for country {self.country} it should be {pincode}")
        
        return self

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, )
    age: int = Field(ge=18, le=69)
    address: AddressCreate

class EmployeePatch(BaseModel):
    name: str = Field(min_length=3, max_length=100, default=None)
    email: EmailStr | None
    password: str = Field(min_length=6, default=None)
    age: int = Field(ge=18, le=69, default=None) 
    address: AddressCreate | None
    

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int | None

    model_config = ConfigDict(from_attributes=True)

class GetEmployeeResponse(EmployeeResponse):
    created_at: datetime
    updated_at: datetime


class EmployeeDepartmentResponse(BaseModel):
    employee_id: int
    department_id: int