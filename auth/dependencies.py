from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from auth import decode_access_token
from auth.schemas import TokenPayload
from exceptions import ForbiddenException, UnauthorizedException
from models.employee import EmployeeRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    payload = decode_access_token(token)

    if payload is None:
        raise UnauthorizedException(detail="User not authorized")
    
    return TokenPayload(**payload)

def require_role(*roles: EmployeeRole):

    def role_checker(current_user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
        if current_user.role not in roles:
            raise ForbiddenException("You do not have permission to perform this action")
        
        return current_user
    
    return role_checker