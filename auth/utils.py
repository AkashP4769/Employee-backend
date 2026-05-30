import bcrypt
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from config import setting

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=setting.jwt_expiry_minutes)
    to_encode["exp"] = expire

    return jwt.encode(to_encode, setting.jwt_secret, algorithm=setting.jwt_algorithm)

def decode_access_token(token: str) -> dict | None:
    print(setting.jwt_algorithm)
    try:
        return jwt.decode(token, setting.jwt_secret, algorithms=setting.jwt_algorithm)
    except JWTError:
        return None