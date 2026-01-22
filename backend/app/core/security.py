from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import get_db
from app.models import sql_models as m

settings = get_settings()

# ---------------------------
# 🔐 Password hashing utilities
# ---------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(plain_password: str) -> bytes:
    hashed_str = pwd_context.hash(plain_password)
    return hashed_str.encode("utf-8")


def verify_password(plain_password: str, stored_hash: bytes | str | None) -> bool:
    if not stored_hash:
        return False
    if isinstance(stored_hash, (bytes, bytearray)):
        stored_hash_str = stored_hash.decode("utf-8", errors="ignore")
    else:
        stored_hash_str = stored_hash
    return pwd_context.verify(plain_password, stored_hash_str)


# ---------------------------
# 🔑 JWT Helpers
# ---------------------------
def create_access_token(sub: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {
        "sub": str(sub),  # ensure string
        "role": role,
        "iat": int(datetime.utcnow().timestamp()),
        "exp": expire,
    }
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    
        return payload
    except JWTError as e:
        print("[JWTError]", e)
        return None


# ---------------------------
# 👤 Current user dependency
# ---------------------------
def get_current_user(
    creds: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db),
) -> m.User:
    if creds is None or (creds.scheme or "").lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    payload = decode_token(creds.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = db.query(m.User).get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user



# ---------------------------
# 👑 Role-based guard
# ---------------------------
def require_admin(current_user: m.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only."
        )
    return current_user


async def get_current_admin(current_user = Depends(get_current_user)):
    """
    Verifică dacă utilizatorul logat are rolul de admin.
    Dacă nu, aruncă o eroare 403 (Forbidden).
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nu aveți permisiunea de a accesa această resursă (doar admin)."
        )
    return current_user