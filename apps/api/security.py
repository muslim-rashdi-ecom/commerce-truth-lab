import os
import hashlib
import hmac
import secrets
import datetime
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import get_jwt_secret_key, get_pseudonymization_salt
from database import get_db
from models import User, Workspace, WorkspaceMember

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

security_bearer = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 with a secure random salt."""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}${pwd_hash.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against stored salt and PBKDF2 hash."""
    try:
        salt, stored_hash = hashed_password.split('$', 1)
        test_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
        return hmac.compare_digest(stored_hash, test_hash)
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_jwt_secret_key(), algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, get_jwt_secret_key(), algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired. Please sign in again.")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.")

def pseudonymize_identifier(raw_value: str, salt: Optional[str] = None) -> str:
    """
    Deterministically pseudonymizes customer PII (email, name, phone, address).
    Returns a consistent opaque pseudonym without storing plaintext data.
    """
    if not raw_value:
        return ""
    v = str(raw_value).strip().lower()
    if not v:
        return ""
    effective_salt = salt or get_pseudonymization_salt()
    digest = hashlib.sha256((v + effective_salt).encode('utf-8')).hexdigest()
    return f"CUST_{digest[:16]}"

async def get_current_user(
    cred: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not cred or not cred.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    payload = decode_access_token(cred.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    
    user = (await db.execute(select(User).where(User.id == user_id))).scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account not found")
    return user

ROLE_HIERARCHY = {"viewer": 1, "auditor": 2, "admin": 3}

async def verify_workspace_access(
    workspace_id: str,
    user: User,
    db: AsyncSession,
    min_role: str = "viewer"
) -> Workspace:
    """
    Enforces strict tenant isolation.
    Verifies that the current user owns or is an active member of the workspace with sufficient role.
    """
    workspace = (await db.execute(select(Workspace).where(Workspace.id == workspace_id))).scalars().first()
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    
    # Owner has full unrestricted permissions
    if workspace.owner_id == user.id:
        return workspace
    
    # Check if registered member with appropriate role
    member = (await db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user.id
        )
    )).scalars().first()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Tenant Isolation: You do not have permission to access this merchant workspace."
        )
        
    member_level = ROLE_HIERARCHY.get(member.role or "viewer", 1)
    required_level = ROLE_HIERARCHY.get(min_role, 1)
    if member_level < required_level:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions: requires at least '{min_role}' role."
        )
        
    return workspace

