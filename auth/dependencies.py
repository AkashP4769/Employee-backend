from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from auth import decode_access_token
from auth.schemas import TokenPayload
from exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    payload = decode_access_token(token)

    if payload is None:
        raise UnauthorizedException(detail="User not authorized")
    
    return TokenPayload(**payload)

