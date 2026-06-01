from pydantic import BaseModel, EmailStr, Field, ConfigDict

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenPayload(BaseModel):
    id: int
    email: str
    role: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str