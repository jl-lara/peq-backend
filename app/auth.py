from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "PEQ_SECRET_KEY_SUPER_SEGURA" # ¡En producción, cambia esto por una variable de entorno!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)